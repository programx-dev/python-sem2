import json
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from src.contracts.task import Task
from src.sources.repository import register_source


def parse_jsonl_file(line: str, path: str, line_no: int) -> dict[str, Any]:
    """
    Распарсить jsonl файл.
    """
    try:
        return json.loads(line)
    except json.JSONDecodeError as error:
        raise ValueError(f"Невалидный JSON в {path}:{line_no}: {error}") from error


@dataclass(frozen=True)
class JsonlSource:
    """
    Генератор задач из JSONl.
    """

    path: Path
    name: str = "file-jsonl"

    def get_tasks(self) -> Iterable[Task]:
        """
        генерирует объекты-задачи из файла JSONL.
        Возвращает по одному.
        """
        with self.path.open("r", encoding="utf-8") as file:
            for line_no, line in enumerate(file, start=1):
                line = line.strip()

                if not line:
                    continue

                task = parse_jsonl_file(line, str(self.path), line_no)
                task_id = str(task.get("id", f"{self.path.name}:{line_no}"))
                task_content = task.get("content", "")

                yield Task(id=task_id, payload=task_content)


@register_source("file-jsonl")
def create_json_source(path: Path) -> JsonlSource:
    return JsonlSource(path=path)
