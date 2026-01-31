import math
from pathlib import Path
import time
import yaml

from rag import pipeline
from haystack.components.builders.answer_builder import AnswerBuilder

from deepeval.models.llms import OllamaModel
from deepeval.metrics import AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase

TEST_FILE = "test/questions.yaml"

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
    contexts = []
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
            include_outputs_from={"llm"},
        )

        contexts.append(
            [d.content for d in response["answer_builder"]["answers"][0].documents]
        )
        responses.append(response["answer_builder"]["answers"][0].data)
    return contexts, responses


ground_truths = [q["answer"] for q in questions_dict]
questions = [q["question"] for q in questions_dict]
contexts, responses = get_contexts_and_responses(questions, pipeline)


metric = AnswerRelevancyMetric(
    model=OllamaModel(model="gemma3", timeout=180),
    async_mode=False,
)

all_results = []


for i, question in enumerate(questions):
    print(f"\nEvaluating question {i + 1}/{len(questions)}")

    try:
        test_case = LLMTestCase(
            input=question,
            actual_output=responses[i],
            expected_output=ground_truths[i],
            retrieval_context=contexts[i],
        )

        metric.measure(test_case)

        result = {
            "id": i,
            "question": question,
            "response": responses[i],
            "metric_name": metric.__name__,
            "score": metric.score,
            "ground_truth": ground_truths[i],
        }
        all_results.append(result)

        print(f"✅ Score: {metric.score:.3f}")

    except Exception as e:
        print(f"❌ Evaluation failed: {e}")

        all_results.append(
            {
                "question": question,
                "score": None,
                "error": str(e),
            }
        )

    time.sleep(1)


valid_scores = [
    r["score"] for r in all_results if isinstance(r.get("score"), (int, float))
]

total_questions = len(all_results)
evaluated_questions = len(valid_scores)

avg_score = (
    sum(valid_scores) / evaluated_questions if evaluated_questions else float("nan")
)
min_score = min(valid_scores) if evaluated_questions else float("nan")
max_score = max(valid_scores) if evaluated_questions else float("nan")
perfect_scores = sum(1 for s in valid_scores if math.isclose(s, 1.0))
perfect_ratio = (
    (perfect_scores / evaluated_questions * 100) if evaluated_questions else 0
)

report_name = Path(TEST_FILE).stem + metric.__name__.replace(" ", "") + ".yaml"

with open(f"reports/{report_name}", "w", encoding="utf-8") as f:
    print(
        f"""
{'='*80}
SUMMARY STATISTICS
{'='*80}
Total questions: {total_questions}
Successfully evaluated: {evaluated_questions}
Average {metric.__name__}: {avg_score:.3f}
Min score: {min_score:.3f}
Max score: {max_score:.3f}
Count(score == 1): {perfect_scores} ({perfect_ratio:.1f}%)
{'='*80}
\n
""",
        file=f,
    )

    yaml.dump(
        all_results,
        f,
        allow_unicode=True,
        sort_keys=False,
        indent=4,
        default_flow_style=False,
    )
