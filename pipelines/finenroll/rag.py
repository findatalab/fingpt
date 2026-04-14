import logging

from haystack_experimental.chat_message_stores.in_memory import InMemoryChatMessageStore
from haystack_experimental.components.retrievers import ChatMessageRetriever
from haystack_experimental.components.writers import ChatMessageWriter
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from haystack import Pipeline
from haystack.components.builders import ChatPromptBuilder
from haystack.components.converters import OutputAdapter
from haystack.components.tools import ToolInvoker
from haystack.dataclasses import ChatMessage
from haystack_integrations.components.generators.ollama import OllamaChatGenerator

from .doc_logger import DocLogger
from .tools import places_tool, price_tool
from ..preprocessor.preprocessor import DOCUMENT_STORE

BASE_MODEL = "qwen3.5"
TOOLS = [price_tool, places_tool]
MAX_TOOL_ITERATIONS = 3
logging.basicConfig(level=logging.DEBUG) # вынести потом в общий конфигурационный файл, либо в main

try:
    with open("pipelines/finenroll/system_prompt.txt", "r", encoding="utf-8") as file:
        system_prompt = file.read()
except FileNotFoundError:
    raise ValueError("Error: The prompt template file was not found.")

# Chat History components
message_store = InMemoryChatMessageStore()
message_retriever = ChatMessageRetriever(message_store)
message_writer = ChatMessageWriter(message_store)


pipeline = Pipeline()

pipeline.add_component(
    "embedder",
    SentenceTransformersTextEmbedder(
        model="deepvk/USER-base", local_files_only=False
    ),
)
pipeline.add_component(
    "retriever", InMemoryEmbeddingRetriever(document_store=DOCUMENT_STORE)
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
) -> str:
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
        return ""

    reply = replies[0]
    tool_iterations = 0

    while getattr(reply, "tool_calls", None) and tool_iterations < MAX_TOOL_ITERATIONS:
        tool_result = tool_invoker.run(messages=[reply])
        tool_messages = tool_result.get("tool_messages", [])
        if not tool_messages:
            break

        current_turn_messages = current_turn_messages + [reply] + tool_messages
        messages_for_llm = messages_for_llm + [reply] + tool_messages

        llm_result = llm.run(messages=messages_for_llm)
        replies = llm_result.get("replies", [])
        if not replies:
            break

        reply = replies[0]
        tool_iterations += 1

    pipeline.get_component("message_writer").run(
        chat_history_id=chat_history_id,
        messages=current_turn_messages + [reply],
    )
    return reply.text or ""
