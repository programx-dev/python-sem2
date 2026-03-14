from pathlib import Path
from typing import List

import typer

import src.sources  # noqa Инициализация реестра источников
from src.contracts.task_source import TaskSource
from src.inbox.core import InboxTasks
from src.sources.repository import REGISTRY

app = typer.Typer(no_args_is_help=True)


def build_active_sources(
    jsonl_files: List[Path], gen_count: int, use_api: bool, api_min: int, api_max: int
) -> List[TaskSource]:
    """Сборка списка источников на основе аргументов CLI."""
    active = []

    if gen_count > 0:
        active.append(REGISTRY["generator"](count=gen_count))

    for path in jsonl_files:
        active.append(REGISTRY["jsonl"](path=path))

    if use_api:
        active.append(REGISTRY["api-stub"](min_tasks=api_min, max_tasks=api_max))

    return active


@app.command()
def read(
    jsonl: List[Path] = typer.Option([], "--jsonl", help="Пути к JSONL файлам."),
    gen: int = typer.Option(0, "--gen", help="Количество генерируемых задач."),
    api: bool = typer.Option(False, "--api", help="Включить API заглушку."),
    api_min: int = typer.Option(1, "--api-min", help="Минимум задач для API."),
    api_max: int = typer.Option(12, "--api-max", help="Максимум задач для API."),
):
    """Чтение и вывод задач из выбранных источников."""

    sources_list = build_active_sources(jsonl, gen, api, api_min, api_max)

    if not sources_list:
        typer.secho(
            "(!) Источники не выбраны. Используйте флаги --gen, --jsonl или --api.",
            fg="yellow",
        )
        raise typer.Exit()

    inbox = InboxTasks(sources_list)

    typer.secho("\n--- Обработка входящих задач ---", fg="cyan")

    count = 0
    try:
        for task in inbox.fetch_all():
            task_id_style = typer.style(task.id, fg="green", bold=True)
            typer.echo(f"ID: {task_id_style:<15} | {task.payload}")
            count += 1

    except Exception as e:
        typer.secho(f"\nОшибка: {e}", fg="red")
        raise typer.Exit(code=1)

    typer.echo(f"\nВыполнено. Всего задач: {count}\n")


@app.command()
def sources():
    """Список всех доступных типов источников."""
    if not REGISTRY:
        typer.echo("Реестр источников пуст.")
        return

    typer.echo("\nДоступные плагины:")
    for i, name in enumerate(sorted(REGISTRY.keys()), 1):
        typer.echo(f" {i}. {typer.style(name, fg='yellow')}")
    typer.echo("")


def main():
    app()


if __name__ == "__main__":
    main()
