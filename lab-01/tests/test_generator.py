import pytest
from src.sources.generator import GeneratorSource, create_generator


def test_generator():
    source = GeneratorSource(7)

    data = [data.payload for data in source.get_tasks()]
    assert len(data) == 7


def test_creating_incorrect_1():
    source = create_generator(-9)

    with pytest.raises(ValueError):
        list(source.get_tasks())


def test_creating_incorrect_2():
    with pytest.raises((ValueError, TypeError)):
        create_generator("Kaban")
