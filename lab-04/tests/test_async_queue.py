import pytest

from src.contracts.task import Task, TaskStatus
from src.inbox.async_task_queue import AsyncTaskQueue


async def mock_source(tasks):
    """Вспомогательный асинхронный источник для тестов."""
    for t in tasks:
        yield t


@pytest.mark.asyncio
async def test_queue_feeding_and_getting():
    """Проверка базового цикла: положили в очередь -> достали из очереди."""
    tasks = [
        Task("1", "Task 1", 10, TaskStatus.NEW, "01.01.2030 00:00:00"),
        Task("2", "Task 2", 20, TaskStatus.NEW, "01.01.2030 00:00:00"),
    ]
    queue = AsyncTaskQueue(mock_source(tasks))
    await queue.start_feeding()

    t1 = await queue.get_task()
    t2 = await queue.get_task()
    sentinel = await queue.get_task()

    assert t1.id == "1"
    assert t2.id == "2"
    assert sentinel is None


@pytest.mark.asyncio
async def test_queue_filtering():
    """Проверка асинхронной фильтрации задач в очереди."""
    tasks = [
        Task("low", "Low Priority", 10, TaskStatus.NEW, "01.01.2030 00:00:00"),
        Task("high", "High Priority", 90, TaskStatus.NEW, "01.01.2030 00:00:00"),
    ]

    queue = AsyncTaskQueue(mock_source(tasks)).filter_by(lambda t: t.priority >= 50)
    await queue.start_feeding()

    t = await queue.get_task()
    assert t.id == "high"
    assert await queue.get_task() is None


@pytest.mark.asyncio
async def test_queue_sentinel_persistence():
    """Проверка, что None остается в очереди для всех воркеров."""
    queue = AsyncTaskQueue(mock_source([]))
    await queue.start_feeding()

    assert await queue.get_task() is None
    assert await queue.get_task() is None
