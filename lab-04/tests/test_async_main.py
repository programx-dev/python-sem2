from typer.testing import CliRunner

from src.inbox.core import AsyncInboxTasks
from src.main import app, build_active_async_inbox

runner = CliRunner()


def test_build_active_async_inbox():
    """Проверка сборки асинхронного контейнера источников."""
    inbox = build_active_async_inbox(
        jsonl_files=[], gen_count=10, use_api=True, api_min=1, api_max=1
    )

    assert isinstance(inbox, AsyncInboxTasks)
    assert len(inbox.sources) == 2  # Generator + API


def test_cli_handlers_command():
    """Проверка команды вывода списка обработчиков."""
    result = runner.invoke(app, ["handlers"])
    assert result.exit_code == 0
    assert "logging" in result.stdout
    assert "email" in result.stdout


def test_cli_async_run_simple_gen():
    """Проверка запуска асинхронного исполнителя через CLI."""
    result = runner.invoke(app, ["async-run", "--gen", "5", "--workers", "2"])

    assert result.exit_code == 0
    assert "Запуск асинхронной обработки" in result.stdout


def test_cli_async_run_no_sources():
    """Проверка поведения при отсутствии источников."""
    result = runner.invoke(app, ["async-run"])
    assert result.exit_code == 0
    assert "Источники не выбраны" in result.stdout
