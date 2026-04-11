"""
Deployable pipeline wrapper for the FinGPT Agent. This wrapper defines two endpoints:
1. POST /fingpt_agent/run - Accepts a user question and returns a direct answer.
2. POST /chat/completions - An OpenAI-compatible endpoint that accepts a list of messages
and returns a direct response from the agent.
"""

from haystack.dataclasses import ChatMessage
from hayhooks import BasePipelineWrapper
from .rag import pipeline as rag_pipeline, run_finenroll_query  # type: ignore


class PipelineWrapper(BasePipelineWrapper):
    def setup(self) -> None:
        self.pipeline = rag_pipeline

    @staticmethod
    def _chat_history_id_from_body(body: dict | None) -> str:
        if not body:
            return "default_chat_session"
        return body.get("chat_history_id") or "default_chat_session"

    @staticmethod
    def _get_last_user_message(messages: list[dict]) -> str:
        for msg in reversed(messages):
            if msg.get("role") == "user":
                content = msg.get("content", "")
                return content if isinstance(content, str) else str(content)
        return ""

    # This will create an OpenAI-compatible /chat/completions endpoint
    def run_chat_completion(self, model: str, messages: list[dict], body: dict) -> str:
        chat_history_id = self._chat_history_id_from_body(body)
        question = self._get_last_user_message(messages)
        return run_finenroll_query(question, chat_history_id=chat_history_id)
