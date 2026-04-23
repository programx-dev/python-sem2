import pytest
from src.sources.api_stub import CONSTANTS, ApiStubSource, create_api_source


def test_api_stub_correct_generation():
    """Проверка генерации точного количества задач и соответствия данных."""
    count = 3
    source = ApiStubSource(count, count)
    tasks = list(source.get_tasks())

    assert len(tasks) == count

    valid_ids = {item["task_id"] for item in CONSTANTS}
    id_to_desc = {item["task_id"]: item["description"] for item in CONSTANTS}

    for task in tasks:
        assert task.id in valid_ids

        assert task.description == id_to_desc[task.id]

        assert task.priority >= 0

        assert task.deadline > task.created_at


def test_create_api_source_range():
    """Проверка генерации случайного количества задач в заданном диапазоне."""
    min_count, max_count = 3, 5

    source = create_api_source(min_count, max_count)
    
    tasks = list(source.get_tasks())
    
    assert min_count <= len(tasks) <= max_count


def test_create_api_source_inverted_range():
    """Проверка корректной обработки диапазона, если min и max перепутаны."""
    min_count, max_count = 5, 3
    
    source = create_api_source(min_count, max_count)
    
    tasks = list(source.get_tasks())
    
    assert 3 <= len(tasks) <= 5


@pytest.mark.parametrize("min_val, max_val", [
    (1, 1),
    (0, 10),
    (5, 5),
    (10, 0)
])
def test_api_stub_parameterized(min_val, max_val):
    """Параметризованный тест для различных границ диапазона."""
    source = create_api_source(min_val, max_val)
    tasks = list(source.get_tasks())
    
    low, high = (min_val, max_val) if min_val <= max_val else (max_val, min_val)

    assert low <= len(tasks) <= high