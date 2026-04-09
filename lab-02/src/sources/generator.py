from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime, timedelta
from random import randint

from src.contracts.task import Task, TaskStatus
from src.sources.repository import register_source


@dataclass(frozen=True, slots=True)
class GeneratorSource:
    """Генерирует задачи программно для тестирования системы."""

    count: int = 5

    def get_tasks(self) -> Iterable[Task]:
        if self.count < 0:
            raise ValueError(
                f"Количество задач не может быть отрицательным: {self.count}"
            )

        for i in range(1, self.count + 1):
            id = f"GEN-{i}"
            description = f"Атоматически сгенерированная задача № {i}"
            priority = randint(1, i)
            status = TaskStatus.NEW
            deadline = datetime.now() + timedelta(days=7)
            created_at = datetime.now()

            yield Task(
                task_id=id,
                description=description,
                priority=priority,
                status=status,
                deadline=deadline,
                created_at=created_at,
            )


@register_source("generator")
def create_generator(count: int = 5) -> GeneratorSource:
    try:
        clean_count = int(count)
    except (ValueError, TypeError):
        raise TypeError(f"Параметр 'count' должен быть числом, получено: {type(count)}")

    if count < 0:
        raise ValueError("Параметр 'count' должен быть неотрицательным")

    return GeneratorSource(count=clean_count)
