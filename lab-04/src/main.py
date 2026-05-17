import asyncio
import logging
from pathlib import Path
from typing import Callable

import typer

import src.sources  # noqa Инициализация реестра источников
from src.contracts.task import Task, TaskStatus
from src.executor import AsyncExecutor
from src.handlers import EmailNotificationHandler, LoggingTaskHandler
from src.inbox.async_task_queue import AsyncTaskQueue
from src.inbox.core import AsyncInboxTasks, InboxTasks
from src.inbox.task_queue import TaskQueue
from src.sources.repository import REGISTRY

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)

app = typer.Typer(name="lab4", no_args_is_help=True)


def filter_status(statuses: list[TaskStatus]) -> Callable[[Task], bool]:
    return lambda task: task.status in statuses


def filter_priority(min_priority: int) -> Callable[[Task], bool]:
    return lambda task: task.priority >= min_priority


def build_active_sources(
    jsonl_files: list[Path], gen_count: int, use_api: bool, api_min: int, api_max: int
) -> list:
    """Сборка списка источников для синхронной работы."""
    active = []
    if gen_count > 0:
        active.append(REGISTRY["generator"](count=gen_count))
    for path in jsonl_files:
        active.append(REGISTRY["jsonl"](path=path))
    if use_api:
        active.append(REGISTRY["api-stub"](min_tasks=api_min, max_tasks=api_max))
    return active


def build_active_async_inbox(
    jsonl_files: list[Path], gen_count: int, use_api: bool, api_min: int, api_max: int
) -> AsyncInboxTasks:
    """Сборка асинхронных источников."""
    inbox = AsyncInboxTasks()
    if gen_count > 0:
        inbox.add_source(REGISTRY["generator"](count=gen_count))
    for path in jsonl_files:
        inbox.add_source(REGISTRY["jsonl"](path=path))
    if use_api:
        inbox.add_source(REGISTRY["api-stub"](min_tasks=api_min, max_tasks=api_max))
    return inbox


@app.command()
def read(
    jsonl: list[Path] = typer.Option([], "--jsonl", help="Пути к JSONL файлам."),
    gen: int = typer.Option(0, "--gen", help="Количество генерируемых задач."),
    api: bool = typer.Option(False, "--api", help="Включить API заглушку."),
    api_min: int = typer.Option(1, "--api-min", help="Минимум задач для API."),
    api_max: int = typer.Option(12, "--api-max", help="Максимум задач для API."),
    min_priority: int = typer.Option(0, "--min-priority"),
    status: list[TaskStatus] = typer.Option([], "--status"),
):
    """Чтение и вывод задач из выбранных источников (синхронно)."""
    sources_list = build_active_sources(jsonl, gen, api, api_min, api_max)

    if not sources_list:
        typer.secho("(!) Источники не выбраны.", fg="yellow")
        raise typer.Exit()

    inbox = InboxTasks(sources_list)
    queue = TaskQueue(inbox)

    if min_priority > 0:
        queue = queue.filter_by(filter_priority(min_priority))
    if status:
        queue = queue.filter_by(filter_status(status))

    typer.secho("\n--- Список задач (синхронно) ---", fg="cyan")
    count = 0
    for task in queue:
        style_id = typer.style(task.id, fg="green", bold=True)
        typer.echo(f"ID: {style_id:<15} | {task.status.name:<12} | {task.description}")
        count += 1
    typer.echo(f"\nВсего задач: {count}\n")


@app.command("async-run")
def async_run_tasks(
    jsonl: list[Path] = typer.Option([], "--jsonl", help="Пути к JSONL файлам."),
    gen: int = typer.Option(0, "--gen", help="Количество генерируемых задач."),
    api: bool = typer.Option(False, "--api", help="Включить API заглушку."),
    api_min: int = typer.Option(1, "--api-min", help="Минимум задач для API."),
    api_max: int = typer.Option(12, "--api-max", help="Максимум задач для API."),
    min_priority: int = typer.Option(0, "--min-priority"),
    status: list[TaskStatus] = typer.Option([], "--status"),
    handlers: list[str] = typer.Option(["logging"], "--handler", "-h"),
    workers: int = typer.Option(
        3, "--workers", help="Количество параллельных воркеров."
    ),
):
    """Асинхронный запуск обработки задач."""
    inbox = build_active_async_inbox(jsonl, gen, api, api_min, api_max)

    if not inbox.sources:
        typer.secho("(!) Источники не выбраны.", fg="yellow")
        raise typer.Exit()

    mapping = {"logging": LoggingTaskHandler(), "email": EmailNotificationHandler()}
    selected_handlers = [mapping[h] for h in handlers if h in mapping]

    if not selected_handlers:
        typer.secho("(!) Нет активных обработчиков.", fg="red")
        raise typer.Exit(1)

    async def entrypoint():
        task_queue = AsyncTaskQueue(inbox.get_async_tasks())

        # Применяем фильтры
        if min_priority > 0:
            task_queue = task_queue.filter_by(filter_priority(min_priority))
        if status:
            task_queue = task_queue.filter_by(filter_status(status))

        # Запуск исполнителя
        async with AsyncExecutor(
            task_queue, selected_handlers, worker_count=workers
        ) as ex:
            await ex.run()

    typer.secho(f"Запуск асинхронной обработки ({workers} воркеров)...", fg="cyan")
    asyncio.run(entrypoint())


@app.command()
def sources():
    """Список всех доступных типов источников."""
    typer.echo("\nДоступные плагины:")
    for name in sorted(REGISTRY.keys()):
        typer.echo(f" - {typer.style(name, fg='yellow')}")


@app.command()
def handlers():
    """Выводит список доступных обработчиков."""
    typer.echo("Доступные обработчики: logging, email")


def main():
    app()


if __name__ == "__main__":
    main()
