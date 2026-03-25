import datetime
import time
from pathlib import Path
from typing import List, Dict, Any
from deepeval.models.llms import OllamaModel
from deepeval.metrics import ContextualPrecisionMetric, ContextualRecallMetric
from deepeval.test_case import LLMTestCase
import yaml

from components.rag import pipeline
from haystack.components.builders.answer_builder import AnswerBuilder


TEST_FILE = "test/questions20.yaml"

try:
    with open(TEST_FILE, "r", encoding="utf-8") as file:
        questions_dict = yaml.safe_load(file)
        # You can now access data like a Python dictionary
        print(f"Success read {len(questions_dict)} questions.")
except FileNotFoundError:
    print("Error: The file was not found.")
except yaml.YAMLError as e:
    print(f"Error parsing YAML file: {e}")

chat_history_id = "test_1"


pipeline.add_component("answer_builder", AnswerBuilder())
pipeline.connect("llm.replies", "answer_builder.replies")
pipeline.connect("retriever", "answer_builder.documents")


def get_contexts_and_responses(questions, pipeline):
    all_contexts = []
    responses = []

    for i, question in enumerate(questions):
        response = pipeline.run(
            data={
                "embedder": {"text": question},
                "prompt_builder": {"query": question},
                "message_retriever": {"chat_history_id": f"chat_{i}"},
                "message_writer": {"chat_history_id": f"chat_{i}"},
                "answer_builder": {"query": question},
            },
            include_outputs_from={"llm", "retriever"},
        )

        docs = response["retriever"]["documents"]

        ranked_contexts = []
        for rank, d in enumerate(docs, start=1):
            ranked_contexts.append({
                "rank": rank,
                "score": getattr(d, "score", None),
                "content": d.content,
                "meta": d.meta,
            })

        all_contexts.append(ranked_contexts)
        responses.append(response["answer_builder"]["answers"][0].data)

        # print(f"\nQuestion {i+1}: {question}")
        # for c in ranked_contexts:
        #     print(f"  Rank {c['rank']} | Score={c['score']} | meta={c['meta']}")
        # print("Response:", responses[-1])
        # print("-" * 60)

    return all_contexts, responses


gold_ids = [list(map(int, q['gold_chunks_id'].split(", "))) for q in questions_dict]
ground_truths = [q['answer'] for q in questions_dict]
questions = [q['question'] for q in questions_dict]
contexts, responses = get_contexts_and_responses(questions, pipeline)

# ----------------------------
# IR metrics by chunk_id
# ----------------------------
def first_relevant_rank_by_chunks_id(ranked_contexts: List[Dict], gold_chunks_id: List[int]) -> int | None:
    for item in ranked_contexts:
        meta = item.get("meta") or {}
        if meta.get("chunk_id") in gold_chunks_id:
            return int(item["rank"])
    return None


def hit_at_k_by_chunks_id(ranked_contexts: List[Dict], gold_chunks_id: List[int], k: int) -> float:
    return 1.0 if first_relevant_rank_by_chunks_id(ranked_contexts[:k], gold_chunks_id) else 0.0


def precision_at_k_by_chunks_id(ranked_contexts: List[Dict], gold_chunks_id: List[int], k: int) -> float:
    relevant = 0
    for item in ranked_contexts[:k]:
        meta = item.get("meta") or {}
        if meta.get("chunk_id") in gold_chunks_id:
            relevant += 1
    return relevant / k


def recall_at_k_by_chunks_id(ranked_contexts: List[Dict], gold_chunks_id: List[int], k: int) -> float:
    relevant = 0
    for item in ranked_contexts[:k]:
        meta = item.get("meta") or {}
        if meta.get("chunk_id") in gold_chunks_id:
            relevant += 1
    return relevant / len(gold_chunks_id)


def reciprocal_rank_by_chunks_id(ranked_contexts: List[Dict], gold_chunks_id: List[int]) -> float:
    r = first_relevant_rank_by_chunks_id(ranked_contexts, gold_chunks_id)
    return 0.0 if r is None else 1.0 / r


# ----------------------------
# LLM-as-judge metrics
# ----------------------------
model_name = "yandex/YandexGPT-5-Lite-8B-instruct-GGUF"
judge_model = OllamaModel(model=model_name, timeout=180)

contextual_precision_metric = ContextualPrecisionMetric(
    model=judge_model, async_mode=False
)
contextual_recall_metric = ContextualRecallMetric(
    model=judge_model, async_mode=False
)


# ----------------------------
# Evaluation loop
# ----------------------------
all_results: List[Dict[str, Any]] = []

# For summary stats
K_VALUES = (3, 5)
hit_at_k = {k: [] for k in K_VALUES}
precision_at_k = {k: [] for k in K_VALUES}
recall_at_k = {k: [] for k in K_VALUES}
mrr = 0.0

for i, question in enumerate(questions):
    print(f"\nEvaluating question {i + 1}/{len(questions)}")

    ranked_ctx = contexts[i]
    ctx_texts = [c["content"] for c in ranked_ctx]
    q_gold_ids = gold_ids[i]

    # --- IR metrics ---
    ir_metrics: Dict[str, Any] = {
        "gold_chunks_id": q_gold_ids,
    }

    if q_gold_ids is not None:
        reciprocal_rank = reciprocal_rank_by_chunks_id(ranked_ctx, q_gold_ids)
        mrr += reciprocal_rank
        ir_metrics['reciprocal_rank'] = reciprocal_rank

        for k in K_VALUES:
            ir_metrics.update({
                f"hit@{k}": hit_at_k_by_chunks_id(ranked_ctx, q_gold_ids, k),
                f"precision@{k}": precision_at_k_by_chunks_id(ranked_ctx, q_gold_ids, k),
                f"recall@{k}": recall_at_k_by_chunks_id(ranked_ctx, q_gold_ids, k)
            })

    print(f"Reciprocal Rank: {ir_metrics['reciprocal_rank']}")
    for k in K_VALUES:
        print(
            f"Hit@{k}={ir_metrics[f"hit@{k}"]} | "
            f"Precision@{k}={ir_metrics[f"precision@{k}"]} | "
            f"Recall@{k}={ir_metrics[f"recall@{k}"]}"
        )

    # --- LLM-as-judge metrics ---
    judge_metrics: Dict[str, Any] = {
        "contextual_precision": {"score": None, "reason": None},
        "contextual_recall": {"score": None, "reason": None},
    }

    result = {
        "id": i,
        "question": question,
        "response": responses[i],
        "ground_truth": ground_truths[i],
        "ir_metrics": ir_metrics,
        "judge_metrics": judge_metrics,
    }

    try:
        test_case = LLMTestCase(
            input=question,
            actual_output=responses[i],
            expected_output=ground_truths[i],
            retrieval_context=ctx_texts,
        )

        contextual_precision_metric.measure(test_case)
        contextual_recall_metric.measure(test_case)

        judge_metrics["contextual_precision"] = {
            "score": contextual_precision_metric.score,
            "reason": contextual_precision_metric.reason,
        }
        judge_metrics["contextual_recall"] = {
            "score": contextual_recall_metric.score,
            "reason": contextual_recall_metric.reason,
        }

        print(f"✅ ContextualPrecision: {contextual_precision_metric.score:.3f}")
        print(f"🧠 Reason: {contextual_precision_metric.reason}")
        print(f"✅ ContextualRecall: {contextual_recall_metric.score:.3f}")
        print(f"🧠 Reason: {contextual_recall_metric.reason}")

    except Exception as e:
        print(f"❌ Error evaluating LLM-as-a-judge metric: {e}")
        result["error"] = str(e)

    all_results.append(result)
    time.sleep(1)

mrr = mrr / len(questions)

# ----------------------------
# Results
# ----------------------------
print("\n" + "=" * 80)
print("FINAL RESULTS (per question)")
print("=" * 80)
print("MRR:", mrr)

for r in all_results:
    print("─" * 50)
    print("Question:", r["question"])
    if "error" in r:
        print("Error:", r["error"])
    print("IR metrics:", r.get("ir_metrics"))
    print("LLM-as-a-judge metrics:", r.get("judge_metrics"))

all_results.insert(0, {"MRR": mrr})

report_name = f"{datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S')}_" + model_name + Path(TEST_FILE).stem + ".yaml"

with open(f"reports/{report_name}", "w", encoding="utf-8") as f:
    yaml.dump(
        all_results,
        f,
        allow_unicode=True,
        sort_keys=False,
        indent=4,
        default_flow_style=False,
    )