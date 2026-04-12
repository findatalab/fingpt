import logging
from enum import Enum
from pathlib import Path
import yaml

logger = logging.getLogger(__name__)

class SourceType(Enum):
    FAQ = 'faq'
    DOCS = 'documents'
    STRUCTURED = 'structured_docs'


def load_sources_config(sources_path: str = "data_files/sources.yaml") -> dict[SourceType, list[Path]]:
    with open(sources_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    data_sources = config.get("data_sources")
    if not isinstance(data_sources, dict):
        raise ValueError("sources.yaml must contain 'data_sources' mapping")

    result = {}
    logger.info("data_sources: %s", data_sources)
    for source_type in SourceType:
        raw_paths = data_sources.get(source_type.value)
        if raw_paths is None:
            logger.info(f"Paths for %s not found", source_type)
            continue

        sources = []
        for path_obj in raw_paths:
            if not path_obj["enabled"]:
                continue
            file_path = Path(path_obj["path"])
            if not file_path.exists():
                logger.info(f"Source file not found: %s", file_path)
                continue
            sources.append(file_path)

        if len(sources) > 0:
            result[source_type] = sources

    return result
