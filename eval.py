import yaml

try:
    with open("test/questions.yaml", "r") as file:
        questions_dict = yaml.safe_load(file)
        # You can now access data like a Python dictionary
        print(f"Success read {len(questions_dict)} questions.")
except FileNotFoundError:
    print("Error: The file was not found.")
except yaml.YAMLError as e:
    print(f"Error parsing YAML file: {e}")

chat_history_id = "test_1"

from rag import pipeline
from haystack.components.builders.answer_builder import AnswerBuilder

pipeline.add_component("answer_builder", AnswerBuilder())
pipeline.connect("llm.replies", "answer_builder.replies")
pipeline.connect("retriever", "answer_builder.documents")


def get_contexts_and_responses(questions, pipeline):
    contexts = []
    responses = []
    for question in questions:
        response = pipeline.run(
            data={
                "embedder": {"text": question},
                "prompt_builder": {"query": question},
                "message_retriever": {"chat_history_id": chat_history_id},
                "message_writer": {"chat_history_id": chat_history_id},
                "answer_builder": {"query": question},
            },
            include_outputs_from={"llm"},
        )

        contexts.append(
            [d.content for d in response["answer_builder"]["answers"][0].documents]
        )
        responses.append(response["answer_builder"]["answers"][0].data)
    return contexts, responses

ground_truths = [q['answer'] for q in questions_dict]
questions = [q['question'] for q in questions_dict]
contexts, responses = get_contexts_and_responses(questions, pipeline)

from haystack import Pipeline
from haystack_integrations.components.evaluators.deepeval import DeepEvalEvaluator, DeepEvalMetric
from deepeval.models.llms import OllamaModel

context_precision_pipeline = Pipeline()
evaluator = DeepEvalEvaluator(
    metric=DeepEvalMetric.CONTEXTUAL_PRECISION, 
    metric_params={
        "model": OllamaModel("gemma3")  
        })

context_precision_pipeline.add_component("evaluator", evaluator)

evaluation_results = context_precision_pipeline.run(
    {"evaluator": {"questions": questions, "contexts": contexts, "ground_truths": ground_truths, "responses": responses}}
)
print(evaluation_results["evaluator"]["results"])
