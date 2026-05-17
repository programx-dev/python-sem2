import asyncio
import logging
from collections.abc import Iterable

from src.contracts.task import Task
from src.contracts.task_handler import TaskHandlerProtocol
from src.inbox.async_task_queue import AsyncTaskQueue

logger = logging.getLogger(__name__)


class AsyncExecutor:
    """
    Асинхронный исполнитель задач.
    Реализует протокол асинхронного контекстного менеджера.
    """

    def __init__(
        self,
        task_queue: AsyncTaskQueue,
        handlers: Iterable[TaskHandlerProtocol],
        worker_count: int = 3,
    ) -> None:
        self._task_queue = task_queue
        self._handlers = list(handlers)
        self._worker_count = worker_count
        self._workers: list[asyncio.Task] = []

    async def __aenter__(self) -> "AsyncExecutor":
        """Инициализация ресурсов при входе в контекст."""
        logger.info("Запуск асинхронного исполнителя...")
        await self._task_queue.start_feeding()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Очистка ресурсов при выходе из контекста."""
        for worker in self._workers:
            if not worker.done():
                worker.cancel()

        if exc_type:
            logger.error(f"Исполнитель завершился с ошибкой: {exc_val}")
        else:
            logger.info("Асинхронный исполнитель успешно завершил работу.")

    async def _worker(self, worker_id: int) -> None:
        """Внутренняя корутина воркера, которая непрерывно обрабатывает задачи."""
        logger.debug(f"Воркер {worker_id} запущен.")
        while True:
            try:
                task: Task | None = await self._task_queue.get_task()

                # Если получили сигнал завершения, выходим из цикла
                if task is None:
                    logger.debug(f"Воркер {worker_id} получил сигнал завершения.")
                    break

                # Выполняем задачу через все зарегистрированные обработчики
                for handler in self._handlers:
                    if isinstance(handler, TaskHandlerProtocol):
                        try:
                            await handler.handle(task)
                        except Exception as e:
                            logger.error(
                                f"[Воркер {worker_id}] Ошибка при обработке задачи {task.id} "
                                f"обработчиком {handler.__class__.__name__}: {e}"
                            )
                    else:
                        logger.warning(
                            f"Обработчик {handler.__class__.__name__} не соответствует протоколу TaskHandlerProtocol."
                        )

            except asyncio.CancelledError:
                logger.info(f"Воркер {worker_id} был принудительно отменен.")
                break
            except Exception as e:
                logger.error(f"Критическая ошибка в воркере {worker_id}: {e}")
                await asyncio.sleep(1)

    async def run(self) -> None:
        """
        Запускает пул воркеров и ожидает их завершения.
        """
        if not self._handlers:
            logger.warning("Нет зарегистрированных обработчиков. Выполнение отменено.")
            return

        for i in range(1, self._worker_count + 1):
            worker_task = asyncio.create_task(self._worker(i))
            self._workers.append(worker_task)

        await asyncio.gather(*self._workers, return_exceptions=True)
