from collections.abc import Sequence, Iterable

from src.contracts.task import Task
from src.contracts.task_source import TaskSource


class InboxApp:
    """
    Класс управления потоком задач.
    """

    def __init__(self, sources: Sequence[TaskSource] | None = None):
        self._sources = sources or []

    def iter_tasks(self) -> Iterable[Task]:
        """
        Получает поток задач из зарегистрированных источников и
        возвращает их по одному.
        """
        for src in self._sources:
            if not isinstance(src, TaskSource):
                raise TypeError("Ресурс обязан удовлетворять протоколу TaskSource.")

            for task in src.get_tasks():
                yield task
