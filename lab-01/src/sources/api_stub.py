from collections.abc import Iterable
from random import choices, randint

from src.contracts.task import Task
from src.sources.repository import register_source

CONSTANTS = [
    {"uuid": "API-0001", "data": "Синхронизация профиля"},
    {"uuid": "API-0002", "data": "Перевод средств"},
    {"uuid": "API-0003", "data": "Редактирование профиля"},
    {"uuid": "API-0004", "data": "Снятие средств"},
    {"uuid": "API-0005", "data": "Авторизация"},
    {"uuid": "API-0006", "data": "Регистрация"},
]


class ApiStubSource:
    """Имитирует получение задач через внешний API."""

    def __init__(self, min_tasks: int = 1, max_tasks: int = 12):
        self.min_tasks = min_tasks
        self.max_tasks = max_tasks

    def get_tasks(self) -> Iterable[Task]:
        count = randint(self.min_tasks, self.max_tasks)

        for item in choices(CONSTANTS, k=count):
            task_id = item.get("uuid")
            payload = item.get("data")

            yield Task(id=str(task_id), payload=payload)


@register_source("api-stub")
def create_api_source(min_tasks: int = 1, max_tasks: int = 12) -> ApiStubSource:
    if min_tasks > max_tasks:
        min_tasks, max_tasks = max_tasks, min_tasks

    return ApiStubSource(min_tasks, max_tasks)
