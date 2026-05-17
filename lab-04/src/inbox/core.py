import asyncio
from collections.abc import AsyncIterator, Sequence
from typing import Iterator, Union

from src.contracts.task import Task
from src.contracts.task_source import TaskSource, TaskSourceProtocol


class InboxTasks:
    """
    Синхронный контейнер для источников задач.
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


class AsyncInboxTasks:
    """
    Асинхронный контейнер для источников задач.
    """

    def __init__(
        self, sources: Sequence[Union[TaskSourceProtocol, TaskSource]] | None = None
    ):
        self._sources: list[Union[TaskSourceProtocol, TaskSource]] = []
        if sources:
            for source in sources:
                self.add_source(source)

    def add_source(self, source: Union[TaskSourceProtocol, TaskSource]) -> None:
        """Добавляет источник задач."""
        self._sources.append(source)

    @property
    def sources(self) -> list[Union[TaskSourceProtocol, TaskSource]]:
        """Список зарегистрированных источников."""
        return self._sources

    async def get_async_tasks(self) -> AsyncIterator[Task]:
        """
        Асинхронно извлекает задачи из источников.
        Умеет работать как с асинхронными, так и с синхронными источниками.
        """
        for source in self._sources:
            # Если источник поддерживает асинхронный протокол
            if isinstance(source, TaskSourceProtocol) and hasattr(
                source, "get_async_tasks"
            ):
                async for task in source.get_async_tasks():
                    yield task

            # Если источник поддерживает синхронный протокол
            elif isinstance(source, TaskSource) and hasattr(source, "get_tasks"):
                for task in source.get_tasks():
                    yield task
                    await asyncio.sleep(0)
            else:
                raise TypeError(
                    f"Объект {type(source).__name__} не поддерживает контракты TaskSourceProtocol или TaskSource"
                )
