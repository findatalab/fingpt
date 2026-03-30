"""
Deployable pipeline wrapper for the FinGPT Agent. This wrapper defines two endpoints:
1. POST /fingpt_agent/run - Accepts a user question and returns a direct answer.
2. POST /chat/completions - An OpenAI-compatible endpoint that accepts a list of messages
and returns a streaming response from the agent.
"""

from collections.abc import AsyncGenerator
from haystack.dataclasses import ChatMessage
from hayhooks import BasePipelineWrapper, async_streaming_generator
from .rag import pipeline as rag_pipeline  # type: ignore


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
    async def run_chat_completion_async(
        self, model: str, messages: list[dict], body: dict
    ) -> str | AsyncGenerator:
        chat_history_id = self._chat_history_id_from_body(body)
        question = self._get_last_user_message(messages)

        return async_streaming_generator(
            pipeline=self.pipeline,
            pipeline_run_args={
                "embedder": {"text": question},
                "prompt_builder": {"query": question},
                "message_retriever": {"chat_history_id": chat_history_id},
                "message_writer": {"chat_history_id": chat_history_id},
            },
            include_outputs_from={"llm"},
            streaming_components=["llm"],
        )
