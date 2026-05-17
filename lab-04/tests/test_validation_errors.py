import pytest

from src.contracts.task import Task, TaskException, TaskStatus
from src.sources.jsonl import JsonlSource


def test_descriptor_priority_validation():
    """Проверка границ приоритета в дескрипторе."""
    with pytest.raises(TaskException, match="от 0 до 100"):
        Task("1", "D", 150, TaskStatus.NEW, "01.01.2030 00:00:00")


def test_descriptor_empty_string():
    """Проверка пустой строки в описании."""
    with pytest.raises(TaskException, match="непустая строка"):
        Task("1", "  ", 10, TaskStatus.NEW, "01.01.2030 00:00:00")


def test_jsonl_sync_errors(tmp_path):
    """Проверка синхронных ошибок в JSONL."""
    file = tmp_path / "bad.jsonl"
    file.write_text("invalid json")
    source = JsonlSource(file)
    with pytest.raises(ValueError):
        list(source.get_tasks())


def test_cli_read_command_full():
    """Тестируем команду read в CLI для покрытия main.py."""
    from typer.testing import CliRunner

    from src.main import app

    runner = CliRunner()
    result = runner.invoke(app, ["read", "--gen", "2", "--status", "new"])
    assert result.exit_code == 0
    assert "Всего задач: 2" in result.stdout


def test_executor_no_handlers():
    """Проверка случая запуска исполнителя без хендлеров."""
    import asyncio

    from src.executor import AsyncExecutor
    from src.inbox.async_task_queue import AsyncTaskQueue

    async def run():
        q = AsyncTaskQueue(None)
        async with AsyncExecutor(q, []) as ex:
            await ex.run()

    asyncio.run(run())
