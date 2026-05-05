import datetime
import time
from pathlib import Path
from typing import List, Dict, Any

import yaml
from deepeval.models.llms import OllamaModel
from deepeval.metrics import (
    FaithfulnessMetric,
    AnswerRelevancyMetric,
)
from deepeval.test_case import LLMTestCase

from pipelines.config import BASE_MODEL
from pipelines.finenroll.rag import run_finenroll_query


TEST_FILE = "test/questions_debug.yaml"
MODEL_JUDGE = "yandex/YandexGPT-5-Lite-8B-instruct-GGUF"


# ----------------------------
# Load test data
# ----------------------------
with open(TEST_FILE, "r", encoding="utf-8") as file:
    questions_dict = yaml.safe_load(file)

print(f"Success read {len(questions_dict)} questions.")

questions = [q["question"] for q in questions_dict]
ground_truths = [q["answer"] for q in questions_dict]


# ----------------------------
# Judge model
# ----------------------------
judge_model = OllamaModel(
    model=MODEL_JUDGE,
    timeout=180,
)


faithfulness_metric = FaithfulnessMetric(
    model=judge_model,
    async_mode=False,
)

answer_relevancy_metric = AnswerRelevancyMetric(
    model=judge_model,
    async_mode=False,
)


# ----------------------------
# Helpers
# ----------------------------
def documents_to_contexts(documents) -> List[str]:
    return [
        doc.content
        for doc in documents
        if getattr(doc, "content", None)
    ]


def mean(values: List[float]) -> float | None:
    return sum(values) / len(values) if values else None


# ----------------------------
# Evaluation loop
# ----------------------------
all_results: List[Dict[str, Any]] = []

faithfulness_scores = []
answer_relevancy_scores = []
correctness_scores = []

for i, question in enumerate(questions):
    print(f"\nEvaluating generation: {i + 1}/{len(questions)}")

    try:
        rag_result = run_finenroll_query(
            question=question,
            chat_history_id=f"deepeval_generation_eval_{i}",
            return_retrieved_documents=True,
        )

        answer = rag_result["answer"]
        documents = rag_result["documents"]
        contexts = documents_to_contexts(documents)
        ground_truth = ground_truths[i]

        test_case = LLMTestCase(
            input=question,
            actual_output=answer,
            expected_output=ground_truth,
            retrieval_context=contexts,
        )

        faithfulness_metric.measure(test_case)
        answer_relevancy_metric.measure(test_case)

        metrics = {
            "faithfulness": {
                "score": faithfulness_metric.score,
                "reason": faithfulness_metric.reason,
            },
            "answer_relevancy": {
                "score": answer_relevancy_metric.score,
                "reason": answer_relevancy_metric.reason,
            }
        }

        faithfulness_scores.append(faithfulness_metric.score)
        answer_relevancy_scores.append(answer_relevancy_metric.score)

        result = {
            "id": i,
            "question": question,
            "answer": answer,
            "ground_truth": ground_truth,
            "contexts": contexts,
            "retrieved_chunks_id": [
                doc.meta.get("chunk_id")
                for doc in documents
                if getattr(doc, "meta", None)
            ],
            "metrics": metrics,
        }

        print("Question:", question)
        print("Answer:", answer)
        print("Ground truth:", ground_truth)
        print("Faithfulness:", faithfulness_metric.score)
        print("Answer relevancy:", answer_relevancy_metric.score)

    except Exception as e:
        result = {
            "id": i,
            "question": question,
            "ground_truth": ground_truths[i],
            "error": str(e),
        }

        print("Evaluation error:", e)

    all_results.append(result)
    time.sleep(1)


# ----------------------------
# Final summary
# ----------------------------
summary = {
    "total_questions": len(questions),
    "generation_model": BASE_MODEL,
    "judge_model": MODEL_JUDGE,
    "faithfulness_mean": mean(faithfulness_scores),
    "answer_relevancy_mean": mean(answer_relevancy_scores)
}


print("\n" + "=" * 80)
print("FINAL DEEPEVAL GENERATION RESULTS")
print("=" * 80)

for key, value in summary.items():
    print(f"{key}: {value}")


# ----------------------------
# Save report
# ----------------------------
Path("reports").mkdir(exist_ok=True)

safe_model_name = BASE_MODEL.replace("/", "_").replace(":", "_")
report_name = (
    f"{datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S')}_"
    f"deepeval_generation_eval_{safe_model_name}_"
    f"{Path(TEST_FILE).stem}.yaml"
)

report = {
    "summary": summary,
    "results": all_results,
}

with open(f"reports/{report_name}", "w", encoding="utf-8") as f:
    yaml.dump(
        report,
        f,
        allow_unicode=True,
        sort_keys=False,
        indent=4,
        default_flow_style=False,
    )

print(f"\nReport saved to reports/{report_name}")