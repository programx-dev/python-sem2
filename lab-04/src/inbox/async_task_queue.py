import asyncio
import logging
from collections.abc import AsyncIterable
from typing import Callable, Optional

from src.contracts.task import Task

logger = logging.getLogger(__name__)


class AsyncTaskQueue:
    """
    Асинхронная очередь задач.
    """

    def __init__(
        self,
        source: AsyncIterable[Task],
        filters: list[Callable[[Task], bool]] | None = None,
    ):
        self._source = source
        self._filters = filters or []
        self._queue: asyncio.Queue[Task | None] = asyncio.Queue()
        self._feed_task: Optional[asyncio.Task] = None

    def filter_by(self, predicate: Callable[[Task], bool]) -> "AsyncTaskQueue":
        """
        Возвращает новую очередь с добавленным фильтром.
        Позволяет строить цепочки: queue.filter_by(f1).filter_by(f2)
        """
        return AsyncTaskQueue(self._source, self._filters + [predicate])

    async def _feed_queue(self) -> None:
        """Внутренняя фоновая задача: читает источник и наполняет очередь."""
        try:
            async for task in self._source:
                # Применяем фильтры
                if all(f(task) for f in self._filters):
                    await self._queue.put(task)
        except Exception as e:
            logger.error(f"Ошибка при наполнении очереди: {e}")
        finally:
            await self._queue.put(None)

    async def start_feeding(self) -> None:
        """Запускает фоновую загрузку задач в очередь."""
        if self._feed_task is None:
            self._feed_task = asyncio.create_task(self._feed_queue())

    async def get_task(self) -> Task | None:
        """
        Извлекает задачу из очереди или None если источник исчерпан.
        """
        task = await self._queue.get()
        self._queue.task_done()

        if task is None:
            await self._queue.put(None)

        return task
