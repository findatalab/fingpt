from pathlib import Path
from typing import List

from haystack import Pipeline, Document
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack.components.writers import DocumentWriter
from haystack.components.converters import MarkdownToDocument, PyPDFToDocument, TextFileToDocument
from haystack.components.preprocessors import DocumentSplitter, DocumentCleaner
from haystack.components.routers import FileTypeRouter
from haystack.components.joiners import DocumentJoiner

from pipelines.config import DOCUMENT_WRITE_POLICY
from pipelines.finenroll.doc_logger import DocLogger


class DocsPreprocessor:
    def __init__(self, embedder_name, document_store):
        self.pipeline = self.__init_pipeline(embedder_name, document_store)

    def run_pipeline(self, sources: List[Path]):
        if not sources:
            return
        self.pipeline.run({
            "file_type_router": {"sources": sources},
        })

    def __init_pipeline(self, embedder_name, document_store):
        supported_mime_types = ["text/plain", "application/pdf", "text/markdown"]
        pipeline = Pipeline()

        pipeline.add_component(
            "file_type_router",
            FileTypeRouter(mime_types=supported_mime_types)
        )
        pipeline.add_component("text_file_converter", TextFileToDocument())
        pipeline.add_component("markdown_converter", MarkdownToDocument())
        pipeline.add_component("pypdf_converter", PyPDFToDocument())
        pipeline.add_component("document_joiner", DocumentJoiner())
        pipeline.add_component("document_cleaner", DocumentCleaner())
        pipeline.add_component(
            "document_splitter",
            DocumentSplitter(
                split_by="word",
                language="ru",
                split_length=200,
                split_overlap=80,
            ),
        )
        pipeline.add_component("log_after_split", DocLogger("after_split", show=10))
        pipeline.add_component("document_embedder", SentenceTransformersDocumentEmbedder(model=embedder_name, local_files_only=True))
        pipeline.add_component("document_writer", DocumentWriter(document_store=document_store, policy=DOCUMENT_WRITE_POLICY))

        pipeline.connect("file_type_router.text/plain", "text_file_converter.sources")
        pipeline.connect("file_type_router.application/pdf", "pypdf_converter.sources")
        pipeline.connect("file_type_router.text/markdown", "markdown_converter.sources")

        pipeline.connect("text_file_converter", "document_joiner")
        pipeline.connect("pypdf_converter", "document_joiner")
        pipeline.connect("markdown_converter", "document_joiner")

        pipeline.connect("document_joiner", "document_cleaner")
        pipeline.connect("document_cleaner", "document_splitter")
        pipeline.connect("document_splitter", "log_after_split")
        pipeline.connect("log_after_split", "document_embedder")
        pipeline.connect("document_embedder", "document_writer")

        return pipeline
