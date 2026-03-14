import pytest
from src.sources.jsonl import JsonlSource


def test_correct(tmp_path):
    correct_file = tmp_path / "correct_file.jsonl"
    correct_file.write_text(
        '{"id": "1", "content": "test1"}\n{"id": "2", "content": "test2"}',
        encoding="utf-8",
    )

    source = JsonlSource(correct_file)

    data = list(source.get_tasks())

    assert data[0].id == "1" and data[0].payload == "test1"
    assert data[1].id == "2" and data[1].payload == "test2"


def test_incorrect_1(tmp_path):
    incorrect_file1 = tmp_path / "incorrect_file1.jsonl"
    incorrect_file1.write_text('{"id": "1", "content": "test"', encoding="utf-8")

    source = JsonlSource(incorrect_file1)

    with pytest.raises(ValueError):
        list(source.get_tasks())


def test_incorrect_2(tmp_path):
    incorrect_file2 = tmp_path / "incorrect_file2.jsonl"
    incorrect_file2.write_text('{"content": "test"}', encoding="utf-8")

    source = JsonlSource(incorrect_file2)

    with pytest.raises(ValueError):
        list(source.get_tasks())


def test_not_exists(tmp_path):
    not_exists_file = tmp_path / "not_exists_file.jsonl"

    source = JsonlSource(not_exists_file)

    with pytest.raises(FileNotFoundError):
        list(source.get_tasks())


def test_jsonl_with_empty_lines(tmp_path):
    file = tmp_path / "empty_lines.jsonl"
    file.write_text(
        '{"id": "1", "content": "t1"}\n\n{"id": "2", "content": "t2"}\n\n',
        encoding="utf-8",
    )

    source = JsonlSource(file)
    data = list(source.get_tasks())

    assert len(data) == 2


def test_not_dir(tmp_path):
    dir = tmp_path / "not_exists_file"
    dir.mkdir()

    source = JsonlSource(dir)

    with pytest.raises(IsADirectoryError):
        list(source.get_tasks())
