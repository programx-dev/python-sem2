from collections.abc import Iterable
from typing import Protocol, runtime_checkable

from src.contracts.task import Task


@runtime_checkable
class TaskSource(Protocol):
    """
    Протокол для объекта-задачи.
    """

    name: str

    def get_tasks(self) -> Iterable[Task]: ...
