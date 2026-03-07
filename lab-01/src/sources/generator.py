from collections.abc import Iterable
from dataclasses import dataclass
from src.contracts.task import Task
from src.sources.repository import register_source


@dataclass(frozen=True)
class GeneratorSource:
    """
    Программный генератор задач.
    """

    count: int = 5
    name: str = "generator"

    def get_tasks(self) -> Iterable[Task]:
        """
        Возвращает по одному count сгенерированных задач.
        """
        for i in range(1, self.count + 1):
            yield Task(id=f"gen-{i}", payload=f"Сгенерированная задача № {i}")


@register_source("generator")
def create_generator_source(count: int = 5) -> GeneratorSource:
    return GeneratorSource(count=count)
