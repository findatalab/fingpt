from datetime import datetime
import logging
from pathlib import Path
import re
from typing import Any

from haystack_experimental.chat_message_stores.in_memory import InMemoryChatMessageStore
from haystack_experimental.components.retrievers import ChatMessageRetriever
from haystack_experimental.components.writers import ChatMessageWriter
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack import Pipeline
from haystack.components.builders import ChatPromptBuilder
from haystack.components.converters import OutputAdapter
from haystack.components.tools import ToolInvoker
from haystack.dataclasses import ChatMessage
from haystack_integrations.components.generators.ollama import OllamaChatGenerator
from haystack_integrations.components.retrievers.chroma import ChromaEmbeddingRetriever

from .doc_logger import DocLogger
from .tools.places_tool import places_tool
from .tools.price_tool import price_tool
from ..config import BASE_MODEL, EMBEDDER_MODEL, RETRIEVER_TOP_K, DOCUMENT_STORE

TOOLS = [price_tool, places_tool]
MAX_TOOL_ITERATIONS = 3
SAFE_MODEL_NAME = BASE_MODEL.replace("/", "_").replace(":", "_")
ROOT_DIR = Path(__file__).resolve().parents[2]
LOG_DIR = ROOT_DIR / "log"
LOG_DIR.mkdir(parents=True, exist_ok=True)

start_time = datetime.now().strftime("%Y-%m-%d--%H-%M-%S")
log_filename = f"finenroll_tool_calls_{SAFE_MODEL_NAME}_{start_time}.log"

logging.basicConfig(
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    level=logging.DEBUG,
)

function_call_logger = logging.getLogger("fingpt.function_calls")
function_call_handler = logging.FileHandler(LOG_DIR / log_filename, encoding="utf-8")
function_call_handler.setLevel(logging.DEBUG)
function_call_handler.setFormatter(
    logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s")
)
if not function_call_logger.handlers:
    function_call_logger.addHandler(function_call_handler)
function_call_logger.propagate = False



def strip_thinking_tags(text: str) -> str:
    """Remove <think>...</think> tags from LLM response."""
    if not text:
        return text
    return re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()


try:
    with open("pipelines/finenroll/system_prompt.txt", "r", encoding="utf-8") as file:
        system_prompt = file.read()
except FileNotFoundError:
    raise ValueError("Error: The prompt template file was not found.")

# Chat History components - replace with db
message_store = InMemoryChatMessageStore()
message_retriever = ChatMessageRetriever(message_store)
message_writer = ChatMessageWriter(message_store)


pipeline = Pipeline()

pipeline.add_component(
    "embedder",
    SentenceTransformersTextEmbedder(
        model=EMBEDDER_MODEL, local_files_only=True
    ),
)
pipeline.add_component(
    "retriever",
    ChromaEmbeddingRetriever(
        document_store=DOCUMENT_STORE,
        top_k=RETRIEVER_TOP_K,
    )
)

pipeline.add_component(
    "retrieved_docs_logger",
    DocLogger(
        label="Retrieved documents",
        show=3,
        show_content=300,
        log_level=logging.DEBUG,
    ),
)

# components to communicate with an LLM
pipeline.add_component(
    "prompt_builder",
    ChatPromptBuilder(
        template=[
            ChatMessage.from_system(system_prompt),
            ChatMessage.from_user(
                """ Используй контекст: 
{% for document in documents %}
    {{ document.content }}
{% endfor %} 

Ответь на вопрос: {{query}}"""
            ),
        ],
        required_variables="*",
    ),
)

pipeline.add_component(
    "llm",
    OllamaChatGenerator(
        model=BASE_MODEL,
        url="http://localhost:11434",
        generation_kwargs={"temperature": 0},
        tools=TOOLS,
    ),
)


# components for chat history retrieval and storage
pipeline.add_component("message_retriever", ChatMessageRetriever(message_store))
pipeline.add_component("message_writer", ChatMessageWriter(message_store))
pipeline.add_component(
    "message_joiner",
    OutputAdapter(
        template="{{ prompt + replies }}", output_type=list[ChatMessage], unsafe=True
    ),
)

# connections
pipeline.connect("embedder.embedding", "retriever.query_embedding")
pipeline.connect("retriever.documents", "retrieved_docs_logger.documents")
pipeline.connect("retrieved_docs_logger.documents", "prompt_builder.documents")

pipeline.connect("prompt_builder.prompt", "message_retriever.current_messages")
pipeline.connect("prompt_builder.prompt", "message_joiner.prompt")
pipeline.connect("message_retriever.messages", "llm.messages")
pipeline.connect("llm.replies", "message_joiner.replies")
pipeline.connect("message_joiner", "message_writer.messages")


tool_invoker = ToolInvoker(tools=TOOLS)


def run_finenroll_query(
    question: str,
    chat_history_id: str = "default_chat_session",
    return_retrieved_documents: bool = False,
) -> str | dict[str, Any]:
    """Run the admissions pipeline with tool execution enabled."""
    embedder_result = pipeline.get_component("embedder").run(text=question)
    retriever_result = pipeline.get_component("retriever").run(
        query_embedding=embedder_result["embedding"]
    )
    logger_result = pipeline.get_component("retrieved_docs_logger").run(
        documents=retriever_result["documents"]
    )
    prompt_result = pipeline.get_component("prompt_builder").run(
        query=question,
        documents=logger_result["documents"],
    )
    current_turn_messages = prompt_result["prompt"]
    history_result = pipeline.get_component("message_retriever").run(
        chat_history_id=chat_history_id,
        current_messages=current_turn_messages,
    )
    messages_for_llm = history_result["messages"]

    llm = pipeline.get_component("llm")
    llm_result = llm.run(messages=messages_for_llm)
    replies: list[ChatMessage] = llm_result.get("replies", [])
    if not replies:
        function_call_logger.info(
            "No replies returned from LLM for question=%s chat_history_id=%s",
            question,
            chat_history_id,
        )
        if return_retrieved_documents:
            return {
                "answer": "",
                "documents": logger_result["documents"],
            }

        return ""

    reply = replies[0]
    tool_iterations = 0

    function_call_logger.info(
        "LLM reply received: tool_calls=%s tool_iterations=%d question=%s",
        getattr(reply, "tool_calls", None),
        tool_iterations,
        question,
    )

    while getattr(reply, "tool_calls", None) and tool_iterations < MAX_TOOL_ITERATIONS:
        function_call_logger.info(
            "Invoking tool iteration %d for reply tool_calls=%s",
            tool_iterations + 1,
            getattr(reply, "tool_calls", None),
        )

        tool_result = tool_invoker.run(messages=[reply])
        tool_messages = tool_result.get("tool_messages", [])

        function_call_logger.info(
            "Tool result iteration %d: tool_messages=%s tool_result_keys=%s",
            tool_iterations + 1,
            [m.text for m in tool_messages],
            list(tool_result.keys()),
        )

        if not tool_messages:
            function_call_logger.warning(
                "No tool messages returned on iteration %d for question=%s",
                tool_iterations + 1,
                question,
            )
            break

        current_turn_messages = current_turn_messages + [reply] + tool_messages
        messages_for_llm = messages_for_llm + [reply] + tool_messages

        llm_result = llm.run(messages=messages_for_llm)
        replies = llm_result.get("replies", [])
        if not replies:
            function_call_logger.warning(
                "No replies returned from LLM after tool invocation iteration %d",
                tool_iterations + 1,
            )
            break

        reply = replies[0]
        tool_iterations += 1
        function_call_logger.info(
            "LLM responded after tool iteration %d: tool_calls=%s",
            tool_iterations,
            getattr(reply, "tool_calls", None),
        )

    pipeline.get_component("message_writer").run(
        chat_history_id=chat_history_id,
        messages=current_turn_messages + [reply],
    )

    function_call_logger.info(
        "Final reply returned for question=%s tool_iterations=%d reply_text=%s",
        question,
        tool_iterations,
        reply.text,
    )

    answer = strip_thinking_tags(reply.text or "")

    if return_retrieved_documents:
        return {
            "answer": answer,
            "documents": logger_result["documents"],
        }

    return answer
