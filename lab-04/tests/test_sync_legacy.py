import pytest

from src.contracts.task import TaskStatus
from src.inbox.core import AsyncInboxTasks, InboxTasks
from src.inbox.task_queue import TaskQueue
from src.sources.generator import GeneratorSource


def test_sync_inbox_and_queue():
    """Тестируем синхронную цепочку: Source -> Inbox -> Queue."""
    source = GeneratorSource(count=3)
    inbox = InboxTasks([source])
    queue = TaskQueue(inbox)

    tasks = list(queue)
    assert len(tasks) == 3
    assert tasks[0].id == "GEN-1"


def test_task_queue_filtering():
    """Тестируем фильтрацию в синхронной очереди."""
    source = GeneratorSource(count=5)
    queue = TaskQueue(source.get_tasks()).filter_by(lambda t: t.priority >= 0)

    tasks = list(queue)
    assert len(tasks) == 5


def test_async_inbox_sync_fallback():
    """Тестируем работу AsyncInboxTasks с обычными (синхронными) источниками."""

    class JustSyncSource:
        def get_tasks(self):
            from src.contracts.task import Task

            yield Task("S1", "Sync", 1, TaskStatus.NEW, "01.01.2030 00:00:00")

    inbox = AsyncInboxTasks([JustSyncSource()])

    async def collect():
        return [t async for t in inbox.get_async_tasks()]

    import asyncio

    tasks = asyncio.run(collect())
    assert len(tasks) == 1
    assert tasks[0].id == "S1"


def test_inbox_invalid_source():
    """Проверка runtime-валидации в InboxTasks."""
    with pytest.raises(TypeError):
        InboxTasks([123])
