from collections.abc import AsyncIterable, Iterable
from typing import Protocol, runtime_checkable

from src.contracts.task import Task


@runtime_checkable
class TaskSource(Protocol):
    """
    Единый поведенческий контракт для синхронных источников задач.
    """

    def get_tasks(self) -> Iterable[Task]:
        """
        Возвращает поток задач из источника.
        """
        ...


@runtime_checkable
class TaskSourceProtocol(Protocol):
    """
    Поведенческий контракт для асинхронных источников задач.
    """

    def get_async_tasks(self) -> AsyncIterable[Task]:
        """
        Асинхронно возвращает поток задач из источника.
        """
        ...
