import asyncio
import logging

from src.contracts.task import Task
from src.contracts.task_handler import TaskHandlerProtocol

logger = logging.getLogger(__name__)


class LoggingTaskHandler(TaskHandlerProtocol):
    """Обработчик задач - логирование задачи."""

    async def handle(self, task: Task) -> None:
        logger.info(
            f"[{self.__class__.__name__}] Обработка задачи: {task.id}, Status: {task.status.value}, Priority: {task.priority}"
        )
        await asyncio.sleep(0.05)  # Иммитация задержки


class EmailNotificationHandler(TaskHandlerProtocol):
    """Обработчик задач - иммитирует отправку по email."""

    async def handle(self, task: Task) -> None:
        if task.status.value == "NEW":
            logger.info(
                f"[{self.__class__.__name__}] Отправка уведомления для задачи {task.id}: {task.description}"
            )
            await asyncio.sleep(0.1)  # Иммитация задержки
        else:
            logger.info(
                f"[{self.__class__.__name__}] Уведомление не требуется для задачи {task.id} (статус: {task.status.value})"
            )
