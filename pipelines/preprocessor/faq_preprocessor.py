import logging
from typing import List, Dict

import yaml
from pathlib import Path
from haystack import Document, Pipeline
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack.components.writers import DocumentWriter

from pipelines.preprocessor.sources_loader import SourceType

logger = logging.getLogger(__name__)

class FaqPreprocessor:
    def __init__(self, embedder_name, document_store):
        self.pipeline = Pipeline()
        self.pipeline.add_component("document_embedder", SentenceTransformersDocumentEmbedder(model=embedder_name, local_files_only=True))
        self.pipeline.add_component("document_writer", DocumentWriter(document_store=document_store))

        self.pipeline.connect("document_embedder.documents", "document_writer.documents")

    def run_pipeline(self, sources: List[Path]):
        documents = []
        supported_extensions = {".yaml", ".yml"}

        for path in sources:
            if path.suffix.lower() not in supported_extensions:
                logger.info("Unsupported file extension: %s", path.name)
                continue

            with open(path, "r", encoding="utf-8") as f:
                faq_file_content = yaml.safe_load(f)

            if not isinstance(faq_file_content, list):
                raise ValueError(f"FAQ file must contain a list: {path}")

            for faq in faq_file_content:
                doc = self.__to_document(faq, path.name)
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

    def __to_document(self, faq_dict: Dict, file_name: str) -> Document:
        faq_id = faq_dict.get("id")
        question = faq_dict.get("question", "")
        answer = faq_dict.get("answer", "")
        references = faq_dict.get("references", [])

        return Document(
            content=answer,
            meta={
                "source_type": SourceType.FAQ.value,
                "file_name": file_name,
                "question_id": faq_id,
                "question": question,
                "references": references,
            },
        )
