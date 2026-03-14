from dataclasses import FrozenInstanceError

import pytest
from src.contracts.task import Task


def test_task_creation():
    task = Task("123", [1, 2, 3])

    assert task.id == "123"
    assert task.payload == [1, 2, 3]


def test_task_immutability():
    task = Task("007", "payload data")

    with pytest.raises(FrozenInstanceError):
        task.id = "777"

    with pytest.raises(FrozenInstanceError):
        task.payload = "000"
