import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

import yaml
from haystack import Pipeline
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack_integrations.components.retrievers.chroma import ChromaEmbeddingRetriever

from pipelines.config import RETRIEVER_TOP_K, EMBEDDER_MODEL
from pipelines.finenroll.rag import DOCUMENT_STORE

TEST_FILE = "test/questions_debug.yaml"
K_VALUES = (1, 3, 5)


# ----------------------------
# Load test data
# ----------------------------
with open(TEST_FILE, "r", encoding="utf-8") as file:
    questions_dict = yaml.safe_load(file)

questions = [q["question"] for q in questions_dict]
print("questions:", questions)
gold_ids = [
    q["gold_chunks_id"]
    for q in questions_dict
]

print("gold_ids:", gold_ids)

# ----------------------------
# Retriever-only pipeline
# ----------------------------
retrieval_pipeline = Pipeline()

retrieval_pipeline.add_component(
    "embedder",
    SentenceTransformersTextEmbedder(
        model=EMBEDDER_MODEL,
        local_files_only=True,
    ),
)

retrieval_pipeline.add_component(
    "retriever",
    ChromaEmbeddingRetriever(
        document_store=DOCUMENT_STORE,
        top_k=RETRIEVER_TOP_K,
    ),
)

retrieval_pipeline.connect(
    "embedder.embedding",
    "retriever.query_embedding",
)


# ----------------------------
# Metrics
# ----------------------------
def first_relevant_rank(
    ranked_contexts: List[Dict[str, Any]],
    gold_chunks_id: List[int],
) -> Optional[int]:
    for item in ranked_contexts:
        meta = item.get("meta") or {}
        if meta.get("chunk_id") in gold_chunks_id:
            return int(item["rank"])
    return None


def hit_at_k(
    ranked_contexts: List[Dict[str, Any]],
    gold_chunks_id: List[int],
    k: int,
) -> float:
    return 1.0 if first_relevant_rank(ranked_contexts[:k], gold_chunks_id) else 0.0


def precision_at_k(
    ranked_contexts: List[Dict[str, Any]],
    gold_chunks_id: List[int],
    k: int,
) -> float:
    top_k = ranked_contexts[:k]
    if not top_k:
        return 0.0

    relevant = sum(
        1
        for item in top_k
        if (item.get("meta") or {}).get("chunk_id") in gold_chunks_id
    )

    return relevant / k


def recall_at_k(
    ranked_contexts: List[Dict[str, Any]],
    gold_chunks_id: List[int],
    k: int,
) -> float:
    if not gold_chunks_id:
        return 0.0

    relevant = sum(
        1
        for item in ranked_contexts[:k]
        if (item.get("meta") or {}).get("chunk_id") in gold_chunks_id
    )

    return relevant / len(gold_chunks_id)


def reciprocal_rank(
    ranked_contexts: List[Dict[str, Any]],
    gold_chunks_id: List[int],
) -> float:
    rank = first_relevant_rank(ranked_contexts, gold_chunks_id)
    return 0.0 if rank is None else 1.0 / rank


# ----------------------------
# Run retrieval
# ----------------------------
all_results: List[Dict[str, Any]] = []

summary = {
    "mrr": 0.0,
    "hit_at_k": {k: [] for k in K_VALUES},
    "precision_at_k": {k: [] for k in K_VALUES},
    "recall_at_k": {k: [] for k in K_VALUES},
}

for i, question in enumerate(questions):
    print(f"\nEvaluating retriever: {i + 1}/{len(questions)}")

    response = retrieval_pipeline.run(
        data={
            "embedder": {"text": question},
        },
        include_outputs_from={"retriever"},
    )
    print("response:", response)
    docs = response["retriever"]["documents"]

    ranked_contexts = []
    for rank, doc in enumerate(docs, start=1):
        ranked_contexts.append(
            {
                "rank": rank,
                "score": getattr(doc, "score", None),
                "content": doc.content,
                "meta": doc.meta,
            }
        )

    q_gold_ids = gold_ids[i]

    rr = reciprocal_rank(ranked_contexts, q_gold_ids)
    summary["mrr"] += rr

    metrics = {
        "gold_chunks_id": q_gold_ids,
        "retrieved_chunks_id": [
            (item.get("meta") or {}).get("chunk_id")
            for item in ranked_contexts
        ],
        "reciprocal_rank": rr,
    }

    for k in K_VALUES:
        h = hit_at_k(ranked_contexts, q_gold_ids, k)
        p = precision_at_k(ranked_contexts, q_gold_ids, k)
        r = recall_at_k(ranked_contexts, q_gold_ids, k)

        metrics[f"hit@{k}"] = h
        metrics[f"precision@{k}"] = p
        metrics[f"recall@{k}"] = r

        summary["hit_at_k"][k].append(h)
        summary["precision_at_k"][k].append(p)
        summary["recall_at_k"][k].append(r)

    result = {
        "id": i,
        "question": question,
        "metrics": metrics,
        "retrieved_contexts": ranked_contexts,
    }

    all_results.append(result)

    print("Gold chunks:", q_gold_ids)
    print("Retrieved chunks:", metrics["retrieved_chunks_id"])
    print("RR:", rr)

    for k in K_VALUES:
        print(
            f"Hit@{k}={metrics[f'hit@{k}']} | "
            f"Precision@{k}={metrics[f'precision@{k}']} | "
            f"Recall@{k}={metrics[f'recall@{k}']}"
        )


# ----------------------------
# Aggregate metrics
# ----------------------------
n = len(questions)

final_summary = {
    "total_questions": n,
    "top_k": RETRIEVER_TOP_K,
    "embedding_model": EMBEDDER_MODEL,
    "mrr": summary["mrr"] / n,
}

for k in K_VALUES:
    final_summary[f"hit@{k}"] = sum(summary["hit_at_k"][k]) / n
    final_summary[f"precision@{k}"] = sum(summary["precision_at_k"][k]) / n
    final_summary[f"recall@{k}"] = sum(summary["recall_at_k"][k]) / n


print("\n" + "=" * 80)
print("FINAL RETRIEVER RESULTS")
print("=" * 80)

for key, value in final_summary.items():
    print(f"{key}: {value}")


# ----------------------------
# Save report
# ----------------------------
# Path("reports").mkdir(exist_ok=True)

safe_model_name = EMBEDDER_MODEL.replace("/", "_")
report_name = (
    f"{datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S')}_"
    f"retriever_eval_{safe_model_name}_"
    f"{Path(TEST_FILE).stem}.yaml"
)

report = {
    "summary": final_summary,
    "results": all_results,
}
print("\n\nREPORT:\n", report)

# with open(f"reports/{report_name}", "w", encoding="utf-8") as f:
#     yaml.dump(
#         report,
#         f,
#         allow_unicode=True,
#         sort_keys=False,
#         indent=4,
#         default_flow_style=False,
#     )
#
# print(f"\nReport saved to reports/{report_name}")