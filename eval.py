import datetime
import time
from pathlib import Path
from typing import List, Dict, Any
from deepeval.models.llms import OllamaModel
from deepeval.metrics import ContextualPrecisionMetric, ContextualRecallMetric
from deepeval.test_case import LLMTestCase
import yaml


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

from components.rag import pipeline
from haystack.components.builders.answer_builder import AnswerBuilder

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


gold_ids = [q['id'] for q in questions_dict]
ground_truths = [q['answer'] for q in questions_dict]
questions = [q['question'] for q in questions_dict]
contexts, responses = get_contexts_and_responses(questions, pipeline)

# ----------------------------
# IR metrics by chunk_id
# ----------------------------
def first_relevant_rank_by_chunk_id(ranked_contexts, gold_id):
    for item in ranked_contexts:
        meta = item.get("meta") or {}
        if meta.get("chunk_id") == gold_id:
            return item["rank"]
    return None


def hit_at_k_by_chunk_id(ranked_contexts, gold_id, k):
    return 1.0 if first_relevant_rank_by_chunk_id(ranked_contexts[:k], gold_id) else 0.0


def precision_at_k_by_chunk_id(ranked_contexts, gold_id, k):
    relevant = 0
    for item in ranked_contexts[:k]:
        meta = item.get("meta") or {}
        if meta.get("chunk_id") == gold_id:
            relevant += 1
    return relevant / k


def mrr_by_chunk_id(ranked_contexts, gold_id):
    r = first_relevant_rank_by_chunk_id(ranked_contexts, gold_id)
    return 0.0 if r is None else 1.0 / r


# ----------------------------
# LLM-as-judge metrics
# ----------------------------
judge_model = OllamaModel(model="gemma3", timeout=180)

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
ir_hit1, ir_hit3 = [], []
ir_p1, ir_p3 = [], []
ir_mrr = []
judge_prec = []
judge_rec = []

for i, question in enumerate(questions):
    print(f"\nEvaluating question {i + 1}/{len(questions)}")

    ranked_ctx = contexts[i]
    ctx_texts = [c["content"] for c in ranked_ctx]
    gold_chunks_id = gold_ids[i]

    # --- IR metrics ---
    ir_metrics = {
        "gold_chunks_id": gold_chunks_id,
        "hit@1": None,
        "hit@3": None,
        "precision@1": None,
        "precision@3": None,
        "mrr": None,
        "first_relevant_rank": None,
    }

    if gold_chunks_id is not None:
        r = first_relevant_rank_by_chunk_id(ranked_ctx, gold_chunks_id)

        ir_metrics.update({
            "first_relevant_rank": r,
            "hit@1": hit_at_k_by_chunk_id(ranked_ctx, gold_chunks_id, 1),
            "hit@3": hit_at_k_by_chunk_id(ranked_ctx, gold_chunks_id, 3),
            "precision@1": precision_at_k_by_chunk_id(ranked_ctx, gold_chunks_id, 1),
            "precision@3": precision_at_k_by_chunk_id(ranked_ctx, gold_chunks_id, 3),
            "mrr": mrr_by_chunk_id(ranked_ctx, gold_chunks_id),
        })

    # --- LLM-as-judge metrics ---
    judge_metrics: Dict[str, Any] = {
        "contextual_precision": {"score": None, "reason": None},
        "contextual_recall": {"score": None, "reason": None},
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

        print(
            f"IR → Hit@1={ir_metrics['hit@1']} | "
            f"Hit@3={ir_metrics['hit@3']} | "
            f"P@1={ir_metrics['precision@1']:.3f} | "
            f"P@3={ir_metrics['precision@3']:.3f} | "
            f"MRR={ir_metrics['mrr']:.3f} | "
            f"Rank={ir_metrics['first_relevant_rank']}"
        )
        print(f"✅ ContextualPrecision: {contextual_precision_metric.score:.3f}")
        print(f"🧠 Reason: {contextual_precision_metric.reason}")
        print(f"✅ ContextualRecall: {contextual_recall_metric.score:.3f}")
        print(f"🧠 Reason: {contextual_recall_metric.reason}")

        result = {
            "id": i,
            "question": question,
            # "contexts": ctx_texts, # contexts[i],
            "response": responses[i],
            "ground_truth": ground_truths[i],
            "ir_metrics": ir_metrics,
            "judge_metrics": judge_metrics,
        }

        all_results.append(result)

        # collect summary
        ir_hit1.append(ir_metrics["hit@1"])
        ir_hit3.append(ir_metrics["hit@3"])
        ir_p1.append(ir_metrics["precision@1"])
        ir_p3.append(ir_metrics["precision@3"])
        ir_mrr.append(ir_metrics["mrr"])
        judge_prec.append(judge_metrics["contextual_precision"]["score"])
        judge_rec.append(judge_metrics["contextual_recall"]["score"])

    except Exception as e:
        print(f"❌ Evaluation failed: {e}")
        all_results.append(
            {
                "question": question,
                "error": str(e),
                "ir_metrics": ir_metrics,
                "judge_metrics": judge_metrics,
            }
        )

        # still collect IR metrics
        ir_hit1.append(ir_metrics["hit@1"])
        ir_hit3.append(ir_metrics["hit@3"])
        ir_p1.append(ir_metrics["precision@1"])
        ir_p3.append(ir_metrics["precision@3"])
        ir_mrr.append(ir_metrics["mrr"])

    time.sleep(1)

# ----------------------------
# Results
# ----------------------------
print("\n" + "=" * 80)
print("FINAL RESULTS (per question)")
print("=" * 80)

for r in all_results:
    print("─" * 50)
    print("Question:", r["question"])
    if "error" in r:
        print("Error:", r["error"])
    print("IR metrics:", r.get("ir_metrics"))
    print("Judge metrics:", r.get("judge_metrics"))

report_name = f"{datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S')}_" + Path(TEST_FILE).stem + ".yaml"

with open(f"reports/{report_name}", "w", encoding="utf-8") as f:
    yaml.dump(
        all_results,
        f,
        allow_unicode=True,
        sort_keys=False,
        indent=4,
        default_flow_style=False,
    )