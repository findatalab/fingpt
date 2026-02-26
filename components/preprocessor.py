from pathlib import Path
from haystack.components.writers import DocumentWriter
from haystack.components.converters import MarkdownToDocument, PyPDFToDocument, TextFileToDocument
from haystack.components.preprocessors import DocumentSplitter, DocumentCleaner
from haystack.components.routers import FileTypeRouter
from haystack.components.joiners import DocumentJoiner
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack import Pipeline
from haystack.document_stores.in_memory import InMemoryDocumentStore
from pathlib import Path

from components.doc_logger import DocLogger

document_store = InMemoryDocumentStore()

file_type_router = FileTypeRouter(
    mime_types=[
        "text/plain",
        "application/pdf",
        "text/markdown"
    ]
)

text_file_converter = TextFileToDocument()
markdown_converter = MarkdownToDocument()
pdf_converter = PyPDFToDocument()

document_joiner = DocumentJoiner()

log_after_split = DocLogger("after_split", show=5000)

document_cleaner = DocumentCleaner()
document_splitter = DocumentSplitter(
    split_by="word",
    language="ru",
    split_length=350,
    split_overlap=80)


document_embedder = SentenceTransformersDocumentEmbedder(
    model="sentence-transformers/all-MiniLM-L6-v2", 
    local_files_only=True)
document_writer = DocumentWriter(document_store)

preprocessing_pipeline = Pipeline()
preprocessing_pipeline.add_component(instance=file_type_router, name="file_type_router")
preprocessing_pipeline.add_component(instance=text_file_converter, name="text_file_converter")
preprocessing_pipeline.add_component(instance=markdown_converter, name="markdown_converter")
preprocessing_pipeline.add_component(instance=pdf_converter, name="pypdf_converter")

preprocessing_pipeline.add_component(instance=document_joiner, name="document_joiner")

preprocessing_pipeline.add_component(instance=document_cleaner, name="document_cleaner")
preprocessing_pipeline.add_component(instance=document_splitter, name="document_splitter")

preprocessing_pipeline.add_component(instance=document_embedder, name="document_embedder")
preprocessing_pipeline.add_component(instance=document_writer, name="document_writer")

preprocessing_pipeline.add_component(instance=log_after_split, name="log_after_split")


preprocessing_pipeline.connect("file_type_router.text/plain", "text_file_converter.sources")
preprocessing_pipeline.connect("file_type_router.application/pdf", "pypdf_converter.sources")
preprocessing_pipeline.connect("file_type_router.text/markdown", "markdown_converter.sources")

preprocessing_pipeline.connect("text_file_converter", "document_joiner")
preprocessing_pipeline.connect("pypdf_converter", "document_joiner")
preprocessing_pipeline.connect("markdown_converter", "document_joiner")

preprocessing_pipeline.connect("document_joiner", "document_cleaner")
preprocessing_pipeline.connect("document_cleaner", "document_splitter")

preprocessing_pipeline.connect("document_splitter", "log_after_split")

preprocessing_pipeline.connect("log_after_split", "document_embedder")

preprocessing_pipeline.connect("document_embedder", "document_writer")


output_dir = "data_files"
all_files = list(Path(output_dir).glob("**/*"))

yaml_files = [p for p in all_files if p.is_file() and p.suffix.lower() in [".yml", ".yaml"]]
other_files = [p for p in all_files if p.is_file() and p.suffix.lower() not in [".yml", ".yaml"]]

preprocessing_pipeline.run({
    "file_type_router": {"sources": other_files}
})
# print(document_store.count_documents())
# print(document_store.filter_documents()[:3])