import logging
from typing import List, Dict

import yaml
from pathlib import Path
from haystack import Document, Pipeline
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack.components.writers import DocumentWriter

from pipelines.config import DOCUMENT_WRITE_POLICY
from pipelines.preprocessor.sources_loader import SourceType


logger = logging.getLogger(__name__)

class StructuredDocsPreprocessor:
    def __init__(self, embedder_name, document_store):
        self.pipeline = Pipeline()
        self.pipeline.add_component("document_embedder", SentenceTransformersDocumentEmbedder(model=embedder_name, local_files_only=True))
        self.pipeline.add_component("document_writer", DocumentWriter(document_store=document_store, policy=DOCUMENT_WRITE_POLICY))

        self.pipeline.connect("document_embedder.documents", "document_writer.documents")

    def run_pipeline(self, sources: List[Path]):
        documents = []
        supported_extensions = {".yaml", ".yml"}

        for path in sources:
            if path.suffix.lower() not in supported_extensions:
                logger.info("Unsupported file extension: %s", path.name)
                continue

            with open(path, "r", encoding="utf-8") as f:
                structured_content = yaml.safe_load(f)

            if not isinstance(structured_content, list):
                raise ValueError(f"StructuredDoc file must contain a list: {path}")

            for content in structured_content:
                doc = self.__to_document(content, path.name)
                documents.append(doc)

        if not documents:
            return

        self.pipeline.run(
            {
                "document_embedder": {
                    "documents": documents
                }
            }
        )

    def __to_document(self, content: Dict, file_name: str) -> Document:
        filename_without_extension = file_name.split(".")[0]
        chunk_id = f"{filename_without_extension}_{content.get('id')}"
        text = content.get("text")
        header = content.get("header")

        return Document(
            content=text,
            meta={
                "source_type": SourceType.STRUCTURED.value,
                "file_name": file_name,
                "chunk_id": chunk_id,
                "header": header,
            },
        )