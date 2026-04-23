import pytest
import json
from src.sources.jsonl import JsonlSource
from src.contracts.task import TaskStatus


def test_correct_parsing(tmp_path):
    """Проверка корректного парсинга валидного JSONL файла."""
    correct_file = tmp_path / "correct_file.jsonl"

    task1 = {
        "task_id": "1", 
        "description": "test1", 
        "priority": 1, 
        "status": "new", 
        "deadline": "01.01.2030 00:00:00"
    }
    task2 = {
        "task_id": "2", 
        "description": "test2", 
        "priority": 2, 
        "status": "done", 
        "deadline": "02.01.2030 00:00:00"
    }
    
    content = f"{json.dumps(task1)}\n{json.dumps(task2)}"
    correct_file.write_text(content, encoding="utf-8")

    source = JsonlSource(correct_file)
    tasks = list(source.get_tasks())

    assert len(tasks) == 2
    assert tasks[0].id == "1"
    assert tasks[0].description == "test1"
    assert tasks[0].status == TaskStatus.NEW
    assert tasks[1].id == "2"
    assert tasks[1].status == TaskStatus.DONE


def test_syntax_error_in_jsonl(tmp_path):
    """Проверка обработки битого JSON (ошибка синтаксиса)."""
    incorrect_file = tmp_path / "incorrect_syntax.jsonl"
    incorrect_file.write_text('{"task_id": "1", "description": "broken}', encoding="utf-8")

    source = JsonlSource(incorrect_file)

    with pytest.raises(ValueError):
        list(source.get_tasks())


def test_missing_required_fields(tmp_path):
    """Проверка обработки JSON, в котором не хватает полей для Task."""
    incorrect_file = tmp_path / "missing_fields.jsonl"
    incorrect_file.write_text('{"task_id": "1", "description": "test"}', encoding="utf-8")

    source = JsonlSource(incorrect_file)

    with pytest.raises(ValueError, match="отсутствуют обязательные поля"):
        list(source.get_tasks())


def test_file_not_found(tmp_path):
    """Проверка поведения, если файла не существует."""
    not_exists_file = tmp_path / "ghost.jsonl"
    source = JsonlSource(not_exists_file)

    with pytest.raises(FileNotFoundError):
        list(source.get_tasks())


def test_jsonl_with_empty_lines(tmp_path):
    """Проверка, что пустые строки между задачами не ломают парсер."""
    file = tmp_path / "empty_lines.jsonl"
    task_data = json.dumps({
        "task_id": "1", "description": "t1", "priority": 1, 
        "status": "new", "deadline": "01.01.2030 00:00:00"
    })
    file.write_text(f"{task_data}\n\n\n{task_data}\n", encoding="utf-8")

    source = JsonlSource(file)
    tasks = list(source.get_tasks())

    assert len(tasks) == 2


def test_path_is_directory(tmp_path):
    """Проверка ошибки, если вместо файла передан путь к папке."""
    my_dir = tmp_path / "some_directory"
    my_dir.mkdir()

    source = JsonlSource(my_dir)

    with pytest.raises((IsADirectoryError, PermissionError)):
        list(source.get_tasks())


def test_invalid_business_logic_in_json(tmp_path):
    """Проверка случая, когда JSON валиден, но дескриптор отклоняет данные."""
    file = tmp_path / "invalid_logic.jsonl"
    bad_task = {
        "task_id": "1", "description": "t1", "priority": 1, "status": "new",
        "created_at": "01.01.2030 00:00:00",
        "deadline": "01.01.2000 00:00:00" 
    }
    file.write_text(json.dumps(bad_task), encoding="utf-8")

    source = JsonlSource(file)
    with pytest.raises(ValueError):
        list(source.get_tasks())