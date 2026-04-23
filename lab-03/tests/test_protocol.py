import pytest
from src.contracts.task_source import TaskSource
from src.sources.generator import GeneratorSource


def test_correct_protocol():
    assert isinstance(GeneratorSource(count=10), TaskSource)


def test_incorrect_protocol_class():
    class FakeTaskSource:
        pass

    assert not isinstance(FakeTaskSource(), TaskSource)


def test_incorrect_protocol_obj():
    assert not isinstance([1, 2, 3], TaskSource)
    assert not isinstance("Это не источник", TaskSource)
