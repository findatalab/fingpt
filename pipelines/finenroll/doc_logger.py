import logging

from haystack import component
from haystack.dataclasses import Document
from typing import List


logger = logging.getLogger(__name__)

@component
class DocLogger:
    """
    DocLogger - это вспомогательный компонент для логирования и отладки.

    Он логирует поток Document объектов без модификации данных, позволяя
    анализировать промежуточные результаты на различных этапах обработки.

    Компонент может быть внедрен в любой узел pipeline для повышения
    наблюдаемости и упрощения отладки.
    """

    def __init__(self, label: str, show: int = 5, show_content: int = 0, log_level: int = logging.INFO):
        self.label = label
        self.show = show
        self.show_content = show_content
        self.log_level = log_level

    @component.output_types(documents=List[Document])
    def run(self, documents: List[Document]):
        logger.log(self.log_level, f"\n=== {self.label} ===")
        docs_to_show = documents[:self.show] if self.show > 0 else documents

        for i, d in enumerate(docs_to_show):
            logger.log(self.log_level, "id: %s\nmeta: %s\n", d.id, d.meta)
            if self.show_content:
                preview = (d.content or "")[: self.show_content].replace("\n", "\\n")
                logger.log(self.log_level, "preview: %s\n", preview)

        return {"documents": documents}