import pytest
from datetime import datetime, timedelta
from src.contracts.task import Task, TaskStatus, TaskException


def test_task_creation():
    """Проверка создания задачи со всеми валидными полями."""
    deadline = (datetime.now() + timedelta(days=1)).strftime("%d.%m.%Y %H:%M:%S")
    
    task = Task(
        task_id="123",
        description="Тестовое описание",
        priority=5,
        status=TaskStatus.NEW,
        deadline=deadline
    )

    assert task.id == "123"
    assert task.description == "Тестовое описание"
    assert task.priority == 5
    assert task.status == TaskStatus.NEW
    assert isinstance(task.created_at, datetime)


def test_task_id_immutability():
    """Проверка, что ID нельзя изменить (свойство без сеттера)."""
    task = Task("007", "desc", 1, TaskStatus.NEW, "01.01.2030 00:00:00")

    with pytest.raises(AttributeError):
        task.id = "777"


def test_task_created_at_immutability():
    """Проверка, что дату создания нельзя изменить (дескриптор read_only)."""
    task = Task("007", "desc", 1, TaskStatus.NEW, "01.01.2030 00:00:00")

    with pytest.raises(TaskException):
        task.created_at = datetime.now()


def test_task_validation_during_update():
    """Проверка, что дескрипторы продолжают валидировать данные при изменении."""
    task = Task("007", "desc", 1, TaskStatus.NEW, "01.01.2030 00:00:00")

    with pytest.raises(TaskException):
        task.description = "   "

    with pytest.raises(TaskException):
        task.priority = -100


def test_deadline_update_validation():
    """Проверка логики дедлайна при обновлении."""
    task = Task("007", "desc", 1, TaskStatus.NEW, "01.01.2030 00:00:00")
    
    past_date = (task.created_at - timedelta(days=1))
    
    with pytest.raises(TaskException):
        task.deadline = past_date