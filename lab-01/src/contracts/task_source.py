from collections.abc import Iterable
from typing import Protocol, runtime_checkable

from src.contracts.task import Task


@runtime_checkable
class TaskSource(Protocol):
    """
    Единый поведенческий контракт для всех источников задач.
    """

    def get_tasks(self) -> Iterable[Task]:
        """
        Возвращает поток задач из источника.
        """
        ...
