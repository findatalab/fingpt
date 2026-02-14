import yaml
from pathlib import Path
from typing import List

from haystack import Document, component
from haystack.dataclasses import ByteStream


@component
class YamlFAQToDocuments:
    @component.output_types(documents=List[Document])
    def run(self, sources: List[str | Path | ByteStream]):
        documents: List[Document] = []
        for src in sources:
            with open(src, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

            if not isinstance(data, list):
                raise ValueError(f"YAML file must contain a list of items. Got: {type(data)} in {src}")
            for item in data:
                if not isinstance(item, dict):
                    continue
                q = (item["question"]).lower()
                a = (item.get("answer") or "").strip()
                refs = item.get("references") or []
                faq_id = item.get("id")

                documents.append(
                    Document(
                        content = f"Вопрос: {q}\nОтвет: {a}",
                        meta={
                            "source_type": "faq",
                            "source_file": str(src),
                            "faq_id": faq_id,
                            "references": refs,
                        },
                    )
                )

        return {"documents": documents}
