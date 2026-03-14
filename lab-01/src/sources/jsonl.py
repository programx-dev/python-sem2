import json
from collections.abc import Iterable
from pathlib import Path

from src.contracts.task import Task
from src.sources.repository import register_source


class JsonlSource:
    """Читает задачи из файла формата JSON Lines."""

    def __init__(self, path: Path | str):
        # Приводим к Path, даже если пришла строка
        self.path = Path(path)

    def _parse_line(self, line: str, line_no: int) -> Task:
        """Внутренний метод для разбора одной строки JSON."""
        try:
            data = json.loads(line)
            if "id" not in data or "content" not in data:
                raise KeyError("отсутствуют обязательные поля 'id' или 'content'")

            return Task(id=str(data["id"]), payload=data["content"])

        except json.JSONDecodeError as e:
            raise ValueError(
                f"Ошибка синтаксиса JSON ({self.path.name}:{line_no})"
            ) from e
        except KeyError as e:
            raise ValueError(
                f"Ошибка структуры данных ({self.path.name}:{line_no})"
            ) from e

    def get_tasks(self) -> Iterable[Task]:
        if not self.path.exists():
            raise FileNotFoundError(f"Файл не найден: {self.path}")

        if not self.path.is_file():
            raise IsADirectoryError(f"Ожидался файл, но это директория: {self.path}")

        try:
            with self.path.open(encoding="utf-8") as f:
                for line_no, line in enumerate(f, 1):
                    clean_line = line.strip()
                    if not clean_line:
                        continue

                    yield self._parse_line(clean_line, line_no)

        except PermissionError:
            raise PermissionError(f"Нет прав на чтение файла: {self.path}")
        except OSError as e:
            raise RuntimeError(f"Системная ошибка при чтении {self.path.name}") from e


@register_source("jsonl")
def create_jsonl(path: Path) -> JsonlSource:
    return JsonlSource(path)
