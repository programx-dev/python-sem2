from collections.abc import Iterable
from src.contracts.task import Task
from src.sources.repository import register_source


class ApiStubSource:
    """
    Генератор задач API заглушка.
    """

    name: str = "api-stub"

    def get_tasks(self) -> Iterable[Task]:
        """
        Имитируем ответ от API в виде списка словарей.
        """
        api_data = [
            {"uuid": "a1", "data": "Sync user profile"},
            {"uuid": "a2", "data": "Process payment #404"},
            {"uuid": "a3", "data": "Delete user profile"},
        ]
        for item in api_data:
            yield Task(id=item["uuid"], payload=item["data"])


@register_source("api-stub")
def create_api_source() -> ApiStubSource:
    return ApiStubSource()
