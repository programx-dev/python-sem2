import pytest
from datetime import datetime, timedelta
from src.inbox.core import InboxTasks
from src.contracts.task import Task, TaskStatus


class SimpleTaskSource:
    """Заглушка источника, генерирующая валидные задачи."""
    def __init__(self, ids: list[int]) -> None:
        self.ids = ids

    def get_tasks(self):
        for i in self.ids:

            yield Task(
                task_id=str(i),
                description=f"Тестовая задача №{i}",
                priority=i,
                status=TaskStatus.NEW,
                deadline=datetime.now() + timedelta(days=1)
            )


@pytest.fixture
def inbox_tasks_fixture():
    task_1 = SimpleTaskSource([1, 2])
    task_2 = SimpleTaskSource([3, 4])
    task_3 = SimpleTaskSource([5, 6])

    return InboxTasks((task_1, task_2, task_3))


def test_inbox_fetches_all_tasks_from_all_sources(inbox_tasks_fixture):
    """Проверка, что Inbox собирает все задачи изо всех источников."""
    tasks = list(inbox_tasks_fixture.fetch_all())
    
    actual_ids = {task.id for task in tasks}

    assert len(tasks) == 6
    assert actual_ids == {"1", "2", "3", "4", "5", "6"}
    
    for task in tasks:
        assert isinstance(task, Task)
        assert task.status == TaskStatus.NEW


def test_invalid_source_sequence_raises_error():
    """Проверка, что InboxTasks падает, если вместо источника передана строка."""
    sources = [SimpleTaskSource([1, 2]), "CSMA/CD"]

    with pytest.raises(TypeError):
        inbox = InboxTasks(sources)

        list(inbox.fetch_all())


def test_inbox_with_empty_source():
    """Проверка работы Inbox, если один из источников пустой."""
    sources = (
        SimpleTaskSource([1, 2]),
        SimpleTaskSource([]),
        SimpleTaskSource([3])
    )
    inbox = InboxTasks(sources)
    tasks = list(inbox.fetch_all())
    
    assert len(tasks) == 3
    assert {t.id for t in tasks} == {"1", "2", "3"}