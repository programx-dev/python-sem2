import json
from collections.abc import Iterable
from pathlib import Path

from src.contracts.task import Task, TaskException, TaskStatus
from src.sources.repository import register_source


class JsonlSource:
    """Читает задачи из файла формата JSON Lines."""

    def __init__(self, path: Path | str):
        # Приводим к Path, даже если пришла строка
        self.path = Path(path)

    def _parse_line(self, line: str, line_no: int) -> Task:
        """Внутренний метод для разбора одной строки JSONL и создания объекта Task."""
        try:
            data = json.loads(line)

            required_fields = {
                "task_id",
                "description",
                "priority",
                "status",
                "deadline",
            }
            missing_fields = required_fields - data.keys()

            if missing_fields:
                raise KeyError(
                    f"отсутствуют обязательные поля: {', '.join(missing_fields)}"
                )

            try:
                data["status"] = TaskStatus(data["status"])
            except ValueError:
                valid_statuses = [s.value for s in TaskStatus]
                raise ValueError(
                    f"недопустимый статус '{data['status']}'. Ожидалось: {valid_statuses}"
                )

            return Task(**data)

        except json.JSONDecodeError as e:
            raise ValueError(f"Ошибка синтаксиса JSON (строка {line_no}): {e}") from e
        except KeyError as e:
            raise ValueError(f"Ошибка структуры данных (строка {line_no}): {e}") from e
        except TaskException as e:
            raise ValueError(
                f"Данные задачи не прошли валидацию (строка {line_no}): {e}"
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
