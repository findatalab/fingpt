# todo use logger instead of print
from haystack import component
from haystack.dataclasses import Document
from typing import List

@component
class DocLogger:
    def __init__(self, label: str, show: int = 3, show_content: int = 0):
        self.label = label
        self.show = show
        self.show_content = show_content

    @component.output_types(documents=List[Document])
    def run(self, documents: List[Document]):
        print(f"\n=== {self.label} ===")
        print("docs:", len(documents))

        for i, d in enumerate(documents[: self.show]):
            content_len = len(d.content or "")
            # print(f"[{i}] content_len={content_len} meta={d.meta}")

            if self.show_content:
                print((d.content or "")[: self.show_content].replace("\n", "\\n"))

        return {"documents": documents}