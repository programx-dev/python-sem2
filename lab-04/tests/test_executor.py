import asyncio

import pytest

from src.contracts.task import Task, TaskStatus
from src.executor import AsyncExecutor
from src.inbox.async_task_queue import AsyncTaskQueue


class MockHandler:
    def __init__(self):
        self.handled_tasks = []

    async def handle(self, task):
        self.handled_tasks.append(task)
        await asyncio.sleep(0.01)


async def mock_source():
    yield Task("T1", "Desc", 1, TaskStatus.NEW, "01.01.2030 00:00:00")


@pytest.mark.asyncio
async def test_executor_runs_and_processes_tasks():
    """Проверка, что исполнитель запускает воркер и обрабатывает задачу."""
    handler = MockHandler()
    queue = AsyncTaskQueue(mock_source())

    async with AsyncExecutor(queue, [handler], worker_count=1) as executor:
        await executor.run()

    assert len(handler.handled_tasks) == 1
    assert handler.handled_tasks[0].id == "T1"


@pytest.mark.asyncio
async def test_executor_error_handling():
    class BrokenHandler:
        async def handle(self, task):
            raise RuntimeError("Boom!")

    good_handler = MockHandler()
    queue = AsyncTaskQueue(mock_source())

    async with AsyncExecutor(queue, [BrokenHandler(), good_handler]) as executor:
        await executor.run()

    assert len(good_handler.handled_tasks) == 1
