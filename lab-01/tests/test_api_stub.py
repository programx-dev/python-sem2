import pytest
from src.sources.api_stub import CONSTANTS, ApiStubSource, create_api_source


def test_correct():
    source = ApiStubSource(3, 3)

    data = [{"uuid": data.id, "data": data.payload} for data in source.get_tasks()]

    assert len(data) == 3

    assert data[0] in CONSTANTS
    assert data[1] in CONSTANTS
    assert data[2] in CONSTANTS


def test_creating_order():
    source = create_api_source(3, 5)

    data = list(source.get_tasks())

    assert 3 <= len(data) <= 5


def test_creating_inver_order():
    source = create_api_source(5, 3)

    data = list(source.get_tasks())

    assert 3 <= len(data) <= 5
