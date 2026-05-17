import json

import pytest

from src.contracts.task import Task
from src.sources.api_stub import ApiStubSource
from src.sources.generator import GeneratorSource
from src.sources.jsonl import JsonlSource


@pytest.mark.asyncio
async def test_generator_async_tasks():
    """Проверка асинхронной генерации задач."""
    count = 5
    source = GeneratorSource(count=count)
    tasks = []
    async for task in source.get_async_tasks():
        tasks.append(task)

    assert len(tasks) == count
    assert all(isinstance(t, Task) for t in tasks)


@pytest.mark.asyncio
async def test_api_stub_async_tasks():
    """Проверка асинхронного получения задач из API-заглушки."""
    source = ApiStubSource(min_tasks=2, max_tasks=2)
    tasks = []
    async for task in source.get_async_tasks():
        tasks.append(task)

    assert len(tasks) == 2


@pytest.mark.asyncio
async def test_jsonl_async_tasks(tmp_path):
    """Проверка асинхронного чтения JSONL."""
    file = tmp_path / "test.jsonl"
    task_data = {
        "task_id": "A1",
        "description": "T",
        "priority": 1,
        "status": "new",
        "deadline": "01.01.2030 00:00:00",
    }
    file.write_text(json.dumps(task_data))

    source = JsonlSource(file)
    tasks = []
    async for task in source.get_async_tasks():
        tasks.append(task)

    assert len(tasks) == 1
    assert tasks[0].id == "A1"
