import csv
import json
from pathlib import Path
from haystack.tools import Tool



def empty_function(
    program_name: str | None = None,
    **kwargs,
) -> str:
    """Возвращает ничего, так как это пустой инструмент-заглушка."""
   

    return json.dumps(
        {
            "query": '',
        },
    )


empty_tool = Tool(
    name="empty_tool",
    description=(
        "Возвращает ничего, так как это пустой инструмент-заглушка."
    ),
    parameters={
        "type": "object",
        "properties": {
            "empty_name": {
                "type": "string",
                "description": "Параметр для пустого инструмента-заглушки",
            }
        },
        "required": ["empty_name"],
    },
    function=empty_function,
)

def test_empty_tool():
    test_program = "Юриспруденция"
    result = empty_function(empty_name=test_program)
    print(result)


if __name__ == "__main__":
    test_empty_tool()
