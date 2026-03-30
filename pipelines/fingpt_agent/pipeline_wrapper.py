import csv
import json
from pathlib import Path
from typing import AsyncGenerator
from haystack.components.agents import Agent
from haystack.dataclasses import ChatMessage
from haystack.tools import Tool
from haystack_integrations.components.generators.ollama import OllamaChatGenerator
from hayhooks import BasePipelineWrapper, async_streaming_generator

try:
    with open("pipelines/fingpt_agent/system_prompt.txt", "r", encoding="utf-8") as file:
        system_prompt = file.read()
except FileNotFoundError:
    raise ValueError("Error: The prompt template file was not found.")

    
PRICE_CSV_PATH = Path(__file__).resolve().parents[2] / "data_files" / "price.csv"


def _normalize(value: str) -> str:
    return " ".join(value.strip().lower().split())


def price_function(program_name: str | None = None, **kwargs) -> str:
    program_name = program_name or kwargs.get("Наименование образовательной программы")
    if not program_name:
        return json.dumps(
            {
                "error": "Argument is required",
                "required": "Наименование образовательной программы",
            },
            ensure_ascii=False,
        )

    if not PRICE_CSV_PATH.exists():
        return json.dumps(
            {
                "error": "Price file not found",
                "path": str(PRICE_CSV_PATH),
            },
            ensure_ascii=False,
        )

    normalized_query = _normalize(program_name)
    matches: list[dict] = []

    with PRICE_CSV_PATH.open("r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            row_program_name = (row.get("Наименование образовательной программы") or "").strip()
            if not row_program_name:
                continue

            if _normalize(row_program_name) == normalized_query:
                matches.append(
                    {
                        "faculty": row.get("Наименование факультета"),
                        "direction_code": row.get("Код направления"),
                        "direction_name": row.get("Наименование направления подготовки"),
                        "program_name": row_program_name,
                        "study_form": row.get("Форма обучения"),
                        "full_price": row.get("Полная стоимость обучения"),
                        "year_1": row.get("1 курс"),
                        "year_2": row.get("2 курс"),
                        "year_3": row.get("3 курс"),
                        "year_4": row.get("4 курс"),
                        "year_5": row.get("5 курс"),
                    }
                )

    if not matches:
        return json.dumps(
            {
                "program_name": program_name,
                "matches": [],
                "message": "No program with this exact name was found",
            },
            ensure_ascii=False,
        )

    return json.dumps(
        {
            "program_name": program_name,
            "matches": matches,
            "count": len(matches),
        },
        ensure_ascii=False,
    )


price_tool = Tool(
    name="price_tool",
    description=(
        "Returns tuition price and metadata by exact value from column "
        "'Наименование образовательной программы'."
    ),
    parameters={
        "type": "object",
        "properties": {
            "Наименование образовательной программы": {
                "type": "string",
                "description": "Exact value of 'Наименование образовательной программы'",
            },
            "program_name": {
                "type": "string",
                "description": "Alias for 'Наименование образовательной программы'",
            },
        },
        "required": ["Наименование образовательной программы"],
    },
    function=price_function,
)


class PipelineWrapper(BasePipelineWrapper):
    def setup(self) -> None:
        self.agent = Agent(
            chat_generator=OllamaChatGenerator(model="qwen3.5"),
            system_prompt=system_prompt,
            tools=[price_tool],
        )

    # This will create a POST /fingpt_agent/run endpoint
    # `question` will be the input argument and will be auto-validated by a Pydantic model
    async def run_api_async(self, question: str) -> str:
        result = await self.agent.run_async(messages=[ChatMessage.from_user(question)])
        return result["last_message"].text

    # This will create an OpenAI-compatible /chat/completions endpoint
    async def run_chat_completion_async(
        self, model: str, messages: list[dict], body: dict
    ) -> AsyncGenerator[str, None]:
        chat_messages = [
            ChatMessage.from_assistant(message) for message in messages
        ]

        return async_streaming_generator(
            pipeline=self.agent,
            pipeline_run_args={
                "messages": chat_messages,
            },
        )
