from collections.abc import Sequence
from typing import Iterator

from src.contracts.task import Task
from src.contracts.task_source import TaskSource


class InboxTasks:
    """
    Компонент для сбора задач из множества источников.
    """

    def __init__(self, sources: Sequence[TaskSource]):
        """
        Выполняет обязательную runtime-проверку контракта.
        """
        self._sources = []

        for source in sources:
            if not isinstance(source, TaskSource):
                raise TypeError(
                    f"Объект {type(source).__name__} не соблюдает контракт TaskSource"
                )

            self._sources.append(source)

    def __iter__(self) -> Iterator[Task]:
        return self.fetch_all()

    def fetch_all(self) -> Iterator[Task]:
        """
        Итерируется по всем источникам и собирает задачи.
        """
        for source in self._sources:
            yield from source.get_tasks()
