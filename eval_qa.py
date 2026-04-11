import os
import re
import yaml
import datetime
import json
import requests
from pipelines.finenroll.rag import BASE_MODEL, run_finenroll_query

# scoring model configuration
MODEL_JUDGE = "yandex/YandexGPT-5-Lite-8B-instruct-GGUF"
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
TEST_FILE = "test/questions20.yaml"


def load_questions(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def call_ollama(prompt: str, timeout: int = 60) -> str:
    headers = {"Content-Type": "application/json"}
    url = f"{OLLAMA_URL}/api/generate"
    payload = {"model": MODEL_JUDGE, "prompt": prompt, "stream": False}
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
    m = re.search(r"([0-9](?:\.\d+)?|9(?:\.0+)?)", text)
    if not m:
        return None
    try:
        v = float(m.group(1))
        return max(0.0, min(9.0, v))
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
            reply = run_finenroll_query(q_text, chat_history_id=f"run_{i}")

            entry = {
                "id": q_id,
                "question": q_text,
                "response": reply,
                "ground_truth": gold,
            }
            # scoring if ground truth exists
            if gold is not None:
                prompt = (
                    "Оцени правильность ответа response путем сравнения с ground_truth по шкале от 0 до 9.\n"
                    "Верни сначала число (0-9), затем краткое объяснение.\n\n"
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
            results.append(
                {
                    "id": q_id,
                    "question": q_text,
                    "response": None,
                    "ground_truth": gold,
                    "error": str(e),
                }
            )
    average_score = (
        sum(average_scores) / len(average_scores) if average_scores else None
    )
    return results, average_score


def save_report(results, average_score=None, base_name=""):
    os.makedirs("reports", exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y-%m-%d--%H-%M-%S")
    filename = f"reports/{ts}{base_name}.yaml"

    question_scores = [
        {
            "id": item.get("id"),
            "question": item.get("question"),
            "score": item.get("score"),
        }
        for item in results
    ]

    report = {
        "base_model": BASE_MODEL,
        "model_judge": MODEL_JUDGE,
        "test_file": TEST_FILE,
        "average_score": average_score,
        "question_scores": question_scores,
        "results": results,
    }

    with open(filename, "w", encoding="utf-8") as f:
        yaml.dump(report, f, allow_unicode=True, sort_keys=False)
    return filename


def main():
    questions = load_questions(TEST_FILE)
    print(f"Loaded {len(questions)} questions from {TEST_FILE}")
    results, average_score = run_all_questions(questions)
    out = save_report(results, average_score)
    print(f"Saved report to {out}")


if __name__ == "__main__":
    main()
