from haystack.document_stores.types import DuplicatePolicy
from haystack_integrations.document_stores.chroma import ChromaDocumentStore

DOCUMENT_STORE = ChromaDocumentStore(
    collection_name="rag_documents",
    persist_path="./chroma_db",
    distance_function="cosine",
)
DOCUMENT_WRITE_POLICY = DuplicatePolicy.OVERWRITE

EMBEDDER_MODEL = "deepvk/USER-base"

BASE_MODEL = "qwen3.5:latest"

RETRIEVER_TOP_K = 5