from typing import Protocol, runtime_checkable

from src.contracts.task import Task


@runtime_checkable
class TaskHandlerProtocol(Protocol):
    """Протокол для обработчика задач."""

    async def handle(self, task: Task) -> None:
        """Асинхронно обрабатывает задачу."""
        ...
