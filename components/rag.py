import os
import dotenv

from haystack_experimental.chat_message_stores.in_memory import InMemoryChatMessageStore
from haystack_experimental.components.retrievers import ChatMessageRetriever
from haystack_experimental.components.writers import ChatMessageWriter
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from haystack import Pipeline
from haystack.components.builders import ChatPromptBuilder
from haystack.components.converters import OutputAdapter
from haystack.dataclasses import ChatMessage
from haystack_integrations.components.generators.ollama import OllamaChatGenerator


from components.preprocessor import document_store

dotenv.load_dotenv('yandex.env')
if "OPENAI_API_KEY" not in os.environ:
    raise ValueError("OPENAI_API_KEY not set in environment variables.")

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
    "retriever", InMemoryEmbeddingRetriever(document_store=document_store)
)

# components to communicate with an LLM
pipeline.add_component(
    "prompt_builder",
    ChatPromptBuilder(
        template=[
            ChatMessage.from_system(
                """Ты консультант для поступающих в Финансовый Университет. 
                Отвечай на вопросы, используя только предоставленный контекст. 
                Если ответа нет в контексте, скажи, что не знаешь ответа.
                Используй простой текстовый формат без разметки."""),
            ChatMessage.from_user(
                """ Контекст:
{% for document in documents %}
    {{ document.content }}
{% endfor %}
Вопрос: {{query}}"""
            ),
        ],
        required_variables="*",
    ),
)

pipeline.add_component(
    "llm",
    OllamaChatGenerator(
        model="yandex/YandexGPT-5-Lite-8B-instruct-GGUF", url="http://localhost:11434"
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
pipeline.connect("retriever", "prompt_builder.documents")

pipeline.connect("prompt_builder.prompt", "message_retriever.current_messages")
pipeline.connect("prompt_builder.prompt", "message_joiner.prompt")
pipeline.connect("message_retriever.messages", "llm.messages")
pipeline.connect("llm.replies", "message_joiner.replies")
pipeline.connect("message_joiner", "message_writer.messages")
