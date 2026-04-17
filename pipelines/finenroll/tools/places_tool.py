import csv
import json
from pathlib import Path
from haystack.tools import Tool


PLACES_CSV_PATH = Path("data_files/tools/places.csv")

def _normalize(value: str) -> str:
    return " ".join(value.strip().lower().split())


def places_function(
    program_name: str | None = None,
    **kwargs,
) -> str:
    """Возвращает количество бюджетных и контрактных мест, а также метаданные по точному значению из `program_name`."""
    search_value = program_name or kwargs.get("Наименование программы подготовки") or kwargs.get("Программа обучения")
    if not search_value:
        return json.dumps(
            {
                "error": "Argument is required",
                "required_any_of": [
                    "program_name"
                ],
            },
            ensure_ascii=False,
        )

    if not PLACES_CSV_PATH.exists():
        return json.dumps(
            {
                "error": "Places file not found",
                "path": str(PLACES_CSV_PATH),
            },
            ensure_ascii=False,
        )

    normalized_query = _normalize(search_value)
    matches: list[dict] = []

    with PLACES_CSV_PATH.open("r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            row_program_name = (row.get("program_name") or "").strip()
            row_direction_name = (row.get("direction_name") or "").strip()
            if not row_direction_name:
                continue

            if _normalize(row_program_name) == normalized_query:
                matches.append(
                    {
                        "study_form": row.get("study_form"),
                        "location": row.get("location"),
                        "direction_code": row.get("code"),
                        "direction_name": row_direction_name,
                        "program_name": row_program_name,
                        "budget_places": row.get("budget_places"),
                        "contract_places": row.get("contract_places"),
                    }
                )

    if not matches:
        return json.dumps(
            {
                "query": search_value,
                "direction_name": search_value,
                "matches": [],
                "message": "Не найдено ни одной специальности с таким точным названием",
            },
            ensure_ascii=False,
        )

    return json.dumps(
        {
            "query": search_value,
            "direction_name": search_value,
            "matches": matches,
            "count": len(matches),
        },
        ensure_ascii=False,
    )


places_tool = Tool(
    name="places_tool",
    description=(
        "Возвращает количество бюджетных и контрактных мест, а также метаданные по точному"
        "значению из столбца 'program_name' (программа или специальность обучения)."
    ),
    parameters={
        "type": "object",
        "properties": {
            "program_name": {
                "type": "string",
                "description": "Значение колонки 'program_name'",
            }
        },
        "required": ["program_name"],
    },
    function=places_function,
)

def test_places_tool():
    test_program = "Юриспруденция"
    result = places_function(program_name=test_program)
    print(result)


if __name__ == "__main__":
    test_places_tool()
