from pathlib import Path
from haystack.components.writers import DocumentWriter
from haystack.components.converters import MarkdownToDocument, PyPDFToDocument, TextFileToDocument
from haystack.components.preprocessors import DocumentSplitter, DocumentCleaner
from haystack.components.routers import FileTypeRouter
from haystack.components.joiners import DocumentJoiner
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack import Pipeline
from haystack.document_stores.in_memory import InMemoryDocumentStore

from .doc_logger import DocLogger

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
log_after_split = DocLogger("after_split", show=10)
document_cleaner = DocumentCleaner()
document_splitter = DocumentSplitter(
    split_by="word",
    language="ru",
    split_length=200,
    split_overlap=20)
            
document_embedder = SentenceTransformersDocumentEmbedder(
    model="deepvk/USER-base", 
    local_files_only=False)
document_writer = DocumentWriter(document_store)

indexing_pipeline = Pipeline()
indexing_pipeline.add_component(instance=file_type_router, name="file_type_router")
indexing_pipeline.add_component(instance=text_file_converter, name="text_file_converter")
indexing_pipeline.add_component(instance=markdown_converter, name="markdown_converter")
indexing_pipeline.add_component(instance=pdf_converter, name="pypdf_converter")

indexing_pipeline.add_component(instance=document_joiner, name="document_joiner")
indexing_pipeline.add_component(instance=document_cleaner, name="document_cleaner")
indexing_pipeline.add_component(instance=document_splitter, name="document_splitter")
indexing_pipeline.add_component(instance=document_embedder, name="document_embedder")
indexing_pipeline.add_component(instance=document_writer, name="document_writer")
indexing_pipeline.add_component(instance=log_after_split, name="log_after_split")

indexing_pipeline.connect("file_type_router.text/plain", "text_file_converter.sources")
indexing_pipeline.connect("file_type_router.application/pdf", "pypdf_converter.sources")
indexing_pipeline.connect("file_type_router.text/markdown", "markdown_converter.sources")

indexing_pipeline.connect("text_file_converter", "document_joiner")
indexing_pipeline.connect("pypdf_converter", "document_joiner")
indexing_pipeline.connect("markdown_converter", "document_joiner")

indexing_pipeline.connect("document_joiner", "document_cleaner")
indexing_pipeline.connect("document_cleaner", "document_splitter")
indexing_pipeline.connect("document_splitter", "log_after_split")
indexing_pipeline.connect("log_after_split", "document_embedder")
indexing_pipeline.connect("document_embedder", "document_writer")

data_dir = "data_files/enroll/txt"
all_files = list(Path(data_dir).glob("**/*"))

yaml_files = [p for p in all_files if p.is_file() and p.suffix.lower() in [".yml", ".yaml"]]
unstructured_files = [p for p in all_files if p.is_file() and p.suffix.lower() not in [".yml", ".yaml"]]

for f in unstructured_files:
    print(f"Processing unstructured file: {f}...")

indexing_pipeline.run({
    "file_type_router": {"sources": unstructured_files}
})

print("Preprocessing completed.")
print(f"Total documents in store: {document_store.count_documents()}")
