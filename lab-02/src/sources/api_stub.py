from collections.abc import Iterable
from random import choices, randint

from src.contracts.task import Task, TaskStatus
from src.sources.repository import register_source

CONSTANTS = [
    {
        "task_id": "API-0001",
        "description": "Синхронизация профиля пользователя с облаком",
        "priority": 1,
        "status": TaskStatus.IN_PROGRESS,
        "deadline": "25.12.2025 12:00:00",
        "created_at": "01.10.2024 09:00:00",
    },
    {
        "task_id": "API-0002",
        "description": "Подготовка модуля: Перевод средств между счетами",
        "priority": 5,
        "status": TaskStatus.NEW,
        "deadline": "15.06.2025 18:30:00",
        "created_at": "10.10.2024 10:00:00",
    },
    {
        "task_id": "API-0003",
        "description": "Редактирование личных данных профиля",
        "priority": 2,
        "status": TaskStatus.NEW,
        "deadline": "20.07.2025 23:59:59",
        "created_at": "11.10.2024 14:20:00",
    },
    {
        "task_id": "API-0004",
        "description": "Снятие наличных через API-шлюз",
        "priority": 10,
        "status": TaskStatus.DONE,
        "deadline": "01.12.2024 10:00:00",
        "created_at": "01.09.2024 08:00:00",
    },
    {
        "task_id": "API-0005",
        "description": "Авторизация по OAuth2 и JWT",
        "priority": 0,
        "status": TaskStatus.IN_PROGRESS,
        "deadline": "31.12.2025 23:59:59",
        "created_at": "12.10.2024 11:00:00",
    },
    {
        "task_id": "API-0006",
        "description": "Регистрация новых корпоративных клиентов",
        "priority": 3,
        "status": TaskStatus.NEW,
        "deadline": "01.01.2026 00:00:00",
        "created_at": "12.10.2024 11:30:00",
    },
]


class ApiStubSource:
    """Имитирует получение задач через внешний API."""

    def __init__(self, min_tasks: int = 1, max_tasks: int = 12):
        self.min_tasks = min_tasks
        self.max_tasks = max_tasks

    def get_tasks(self) -> Iterable[Task]:
        count = randint(self.min_tasks, self.max_tasks)

        for item in choices(CONSTANTS, k=count):
            yield Task(**item)


@register_source("api-stub")
def create_api_source(min_tasks: int = 1, max_tasks: int = 12) -> ApiStubSource:
    if min_tasks > max_tasks:
        min_tasks, max_tasks = max_tasks, min_tasks

    return ApiStubSource(min_tasks, max_tasks)
