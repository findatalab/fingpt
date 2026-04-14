import logging

from haystack.document_stores.in_memory import InMemoryDocumentStore

from pipelines.preprocessor.docs_preprocessor import DocsPreprocessor
from pipelines.preprocessor.faq_preprocessor import FaqPreprocessor
from pipelines.preprocessor.sources_loader import load_sources_config, SourceType
from pipelines.preprocessor.structured_docs_preprocessor import StructuredDocsPreprocessor


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

EMBEDDER_NAME = "sentence-transformers/all-MiniLM-L6-v2"

DOCUMENT_STORE = InMemoryDocumentStore()

sources_map = load_sources_config("../../data_files/sources.yaml")

preprocessors_mapping = {
    SourceType.FAQ: FaqPreprocessor(embedder_name=EMBEDDER_NAME, document_store=DOCUMENT_STORE),
    SourceType.DOCS: DocsPreprocessor(embedder_name=EMBEDDER_NAME, document_store=DOCUMENT_STORE),
    SourceType.STRUCTURED: StructuredDocsPreprocessor(embedder_name=EMBEDDER_NAME, document_store=DOCUMENT_STORE),
}

for source_type, sources  in sources_map.items():
    preprocessor = preprocessors_mapping[source_type]
    preprocessor.run_pipeline(sources)

logger.info("Preprocessing completed")
logger.info(f"Total documents in store: %d", DOCUMENT_STORE.count_documents())