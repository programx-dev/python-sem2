import sys
from collections.abc import Iterable
from src.contracts.task import Task
from src.sources.repository import register_source
from typer import echo


class StdinSource:
    """
    Генератор задач, вводимих из потока ввода.
    """

    name: str = "stdin"

    def get_tasks(self) -> Iterable[Task]:
        """
        Считывает построчно задачи в формате 'id:payload' до нажатия Ctrl+D.
        """
        echo("Введите задачу в формате 'id:payload' (Ctrl+D для конца ввода):")

        for line in sys.stdin:
            if ":" in line:
                tid, payload = line.strip().split(":", 1)
                yield Task(id=tid, payload=payload)


@register_source("stdin")
def create_stdin_source() -> StdinSource:
    return StdinSource()
