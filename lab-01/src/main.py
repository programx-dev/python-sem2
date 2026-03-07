from pathlib import Path
from typing import Any
import typer
from typer import Typer

from src.inbox.core import InboxApp
from src.sources.repository import REGISTRY

cli = Typer(no_args_is_help=True)


@cli.command("plugins")
def plugins_list() -> None:
    typer.echo("Доступные расширения:")
    for name in sorted(REGISTRY):
        typer.echo(name)


def _build_sources(
    stdin: bool, jsonl: list[Path], gen_count: int, use_api: bool
) -> list[Any]:
    """
    Создать список генераторов задач, из существующих фабрик.
    """
    sources: list[Any] = []

    if stdin:
        sources.append(REGISTRY["stdin"]())
    if use_api:
        sources.append(REGISTRY["api-stub"]())
    if gen_count > 0:
        sources.append(REGISTRY["generator"](count=gen_count))
    for path in jsonl:
        sources.append(REGISTRY["file-jsonl"](path))

    return sources


@cli.command("read")
def read(
    stdin: bool = typer.Option(False, "--stdin", help="Читать из потока ввода"),
    jsonl: list[Path] = typer.Option(
        default_factory=list, exists=True, help="Читать из JSONL файлов"
    ),
    gen: int = typer.Option(0, "--gen", help="Программно сгенерировать N задач"),
    api: bool = typer.Option(
        False, "--api", help="Использовать генератор API заглушку"
    ),
    contains: str | None = typer.Option(
        None, "--contains", help="Фильтрация по подстроке (нечуствителен к регистру)"
    ),
):
    raw_sources = _build_sources(stdin, jsonl, gen, api)
    inbox = InboxApp(raw_sources)
    count = 0

    for task in inbox.iter_tasks():
        if contains and contains.lower() not in str(task.payload).lower():
            continue

        count += 1
        typer.echo(f"ID: {task.id:<10} | Полезные данные: {task.payload}")

    typer.echo(f"\nОбработанных задач: {count}")


def main():
    cli()


if __name__ == "__main__":
    main()
