import pytest
from src.sources.generator import GeneratorSource, create_generator
from src.contracts.task import Task


def test_generator_emits_correct_number_of_tasks():
    """Проверка, что генератор создает ровно столько задач, сколько запрошено."""
    count = 7
    source = GeneratorSource(count)
    
    tasks = list(source.get_tasks())
    
    assert len(tasks) == count
    for task in tasks:
        assert isinstance(task, Task)

        assert isinstance(task.description, str)
        assert len(task.description) > 0


@pytest.mark.parametrize("invalid_count", [-1, -9, -100])
def test_generator_with_negative_count(invalid_count):
    """Проверка обработки отрицательного количества задач."""
    with pytest.raises(ValueError):
        create_generator(invalid_count)


@pytest.mark.parametrize("invalid_input", [
    "Kaban", 
    [1, 2], 
    None, 
    "7"
])
def test_generator_invalid_types(invalid_input):
    """Проверка передачи некорректных типов данных вместо числа."""
    with pytest.raises((ValueError, TypeError)):
        create_generator(invalid_input)


def test_generated_tasks_validity():
    """Проверка, что сгенерированные задачи проходят внутреннюю валидацию Task."""
    count = 3
    source = GeneratorSource(count)
    tasks = list(source.get_tasks())

    for task in tasks:
        assert isinstance(task.priority, int)

        assert task.priority >= 0
        
        assert task.deadline > task.created_at