import os
import re
import yaml
import datetime
import json
import requests
from components.rag import pipeline

# scoring model configuration
MODEL = "yandex/YandexGPT-5-Lite-8B-instruct-GGUF"
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
TEST_FILE = "test/questions20.yaml"


def load_questions(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def call_ollama(prompt: str, timeout: int = 60) -> str:
    headers = {"Content-Type": "application/json"}
    url = f"{OLLAMA_URL}/api/generate"
    payload = {"model": MODEL, "prompt": prompt, "stream": False}
    resp = requests.post(url, json=payload, headers=headers, timeout=timeout)
    resp.raise_for_status()
    j = resp.json()
    for key in ("response", "output", "text"):
        if key in j and isinstance(j[key], str):
            return j[key]
    if "choices" in j and isinstance(j["choices"], list) and j["choices"]:
        c = j["choices"][0]
        if isinstance(c, dict):
            return c.get("message", {}).get("content") or c.get("text") or json.dumps(c)
    return json.dumps(j, ensure_ascii=False)


def extract_score(text: str) -> float | None:
    if not text or text.startswith("ERROR:"):
        return None
    m = re.search(r"([1-9](?:\.\d+)?|10(?:\.0+)?)", text)
    if not m:
        return None
    try:
        v = float(m.group(1))
        return max(1.0, min(10.0, v))
    except Exception:
        return None


def run_all_questions(questions):
    results = []
    average_scores = []
    for i, q in enumerate(questions):
        q_text = q.get("question") if isinstance(q, dict) else str(q)
        gold = q.get("answer") if isinstance(q, dict) else None
        q_id = q.get("id") if isinstance(q, dict) else i

        try:
            res = pipeline.run(
                data={
                    "embedder": {"text": q_text},
                    "prompt_builder": {"query": q_text},
                    "message_retriever": {"chat_history_id": f"run_{i}"},
                    "message_writer": {"chat_history_id": f"run_{i}"},
                },
                include_outputs_from={"llm"},
            )

            reply = None
            try:
                reply = res["llm"]["replies"][0].text
            except Exception:
                reply = str(res.get("llm"))

            entry = {
                "id": q_id,
                "question": q_text,
                "response": reply,
                "ground_truth": gold,
            }
            # scoring if ground truth exists
            if gold is not None:
                prompt = (
                    "Оцени правильность ответа response путем сравнения с ground_truth по шкале от 1 до 10.\n"
                    "Верни сначала число (1-10), затем краткое объяснение.\n\n"
                    f"ground_truth:\n{gold}\n\nresponse:\n{reply}\n"
                )
                try:
                    out = call_ollama(prompt)
                except Exception as e:
                    out = f"ERROR: {e}"
                entry["score"] = extract_score(out)
                entry["score_reason"] = out
                if entry["score"] is not None:
                    average_scores.append(entry["score"])

            results.append(entry)

            print(f"[{i+1}/{len(questions)}] OK: saved response for id={q_id}")
            if "score" in entry:
                print(f"    score={entry['score']}")

        except Exception as e:
            print(f"[{i+1}/{len(questions)}] ERROR: {e}")
            results.append({
                "id": q_id,
                "question": q_text,
                "response": None,
                "ground_truth": gold,
                "error": str(e),
            })
    average_score = sum(average_scores) / len(average_scores) if average_scores else None
    return results, average_score


def save_report(results, average_score=None, base_name=TEST_FILE.rsplit("/", 1)[-1].rsplit(".", 1)[0]):
    os.makedirs("reports", exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    filename = f"reports/{ts}_{base_name}.yaml"
    with open(filename, "w", encoding="utf-8") as f:
        yaml.dump({"average_score": average_score, "results": results}, f, allow_unicode=True, sort_keys=False)
    return filename


def main():
    questions = load_questions(TEST_FILE)
    print(f"Loaded {len(questions)} questions from {TEST_FILE}")
    results, average_score = run_all_questions(questions)
    out = save_report(results, average_score)
    print(f"Saved report to {out}")


if __name__ == "__main__":
    main()
