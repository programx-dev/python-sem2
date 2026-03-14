from collections.abc import Iterable
from dataclasses import dataclass
from random import randint

from src.contracts.task import Task
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
            yield Task(id=f"GEN-{i}", payload=f"Случайное число: {randint(1, 1024)}")


@register_source("generator")
def create_generator(count: int = 5) -> GeneratorSource:
    try:
        clean_count = int(count)
    except (ValueError, TypeError):
        raise TypeError(f"Параметр 'count' должен быть числом, получено: {type(count)}")

    return GeneratorSource(count=clean_count)
