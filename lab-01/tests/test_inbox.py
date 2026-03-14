import pytest
from src.inbox.core import InboxTasks
from src.contracts.task import Task


class SimpleTaskSource:
    def __init__(self, data: list[int | None]) -> None:
        self.data = data

    def get_tasks(self):
        for data in self.data:
            yield Task(id=str(data), payload=data)


@pytest.fixture
def inbox_tasks_fixture():
    task_1 = SimpleTaskSource([1, 2])
    task_2 = SimpleTaskSource([3, 4])
    task_3 = SimpleTaskSource([5, 6])

    return InboxTasks((task_1, task_2, task_3))


def test_inbox_correct(inbox_tasks_fixture):
    data = list(inbox_tasks_fixture.fetch_all())
    actual_payloads = {task.payload for task in data}

    assert len(actual_payloads) == 6
    assert {1, 2, 3, 4, 5, 6} == set(actual_payloads)  # порядок не важен


def test_invalid_sequince():
    sources = [SimpleTaskSource([1, 2]), "CSMA/CD"]

    with pytest.raises(TypeError):
        InboxTasks(sources)
