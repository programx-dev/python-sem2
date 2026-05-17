import asyncio
from datetime import datetime, timedelta

import pytest

from src.contracts.task import Task, TaskStatus
from src.sources.generator import GeneratorSource, create_generator
from src.sources.jsonl import JsonlSource


def test_task_properties():
    """Покрываем свойства is_overdue и remaining_time в Task."""
    # Задача в будущем
    future_dt = datetime.now() + timedelta(days=1)
    task = Task("T1", "Desc", 1, TaskStatus.NEW, future_dt)
    assert not task.is_overdue
    assert task.remaining_time.total_seconds() > 0

    # Просроченная задача
    task._deadline = datetime.now() - timedelta(days=1)
    assert task.is_overdue


def test_generator_validation_errors():
    """Покрываем ошибки в GeneratorSource (те самые Missing lines)."""
    with pytest.raises(ValueError):
        list(GeneratorSource(count=-1).get_tasks())

    with pytest.raises(ValueError):

        async def run():
            async for t in GeneratorSource(count=-1).get_async_tasks():
                pass

        asyncio.run(run())

    with pytest.raises(TypeError):
        create_generator("not an int")
    with pytest.raises(ValueError):
        create_generator(-5)


def test_jsonl_sync_iteration(tmp_path):
    """Покрываем синхронный метод get_tasks в JsonlSource."""
    import json

    f = tmp_path / "sync.jsonl"
    task = {
        "task_id": "S1",
        "description": "D",
        "priority": 1,
        "status": "new",
        "deadline": "01.01.2030 00:00:00",
    }
    f.write_text(json.dumps(task))

    source = JsonlSource(f)
    tasks = list(source.get_tasks())
    assert len(tasks) == 1
