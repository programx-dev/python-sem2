from pathlib import Path

import pytest
from src.main import app, build_active_sources
from src.sources.api_stub import ApiStubSource
from src.sources.generator import GeneratorSource
from src.sources.jsonl import JsonlSource
from typer.testing import CliRunner

runner = CliRunner()


def test_build_active_sources_generator_only():
    sources = build_active_sources(
        jsonl_files=[], gen_count=5, use_api=False, api_min=1, api_max=1
    )

    assert len(sources) == 1
    assert isinstance(sources[0], GeneratorSource)
    assert sources[0].count == 5


def test_build_active_sources_api_only():
    sources = build_active_sources([], 0, True, 3, 3)

    assert len(sources) == 1
    assert isinstance(sources[0], ApiStubSource)
    assert sources[0].min_tasks == 3


def test_build_active_sources_multiple_jsonl():
    paths = [Path("test1.jsonl"), Path("test2.jsonl")]
    sources = build_active_sources(paths, 0, False, 1, 1)

    assert len(sources) == 2
    for s in sources:
        assert isinstance(s, JsonlSource)


def test_build_active_sources_empty():
    sources = build_active_sources([], 0, False, 1, 1)
    assert len(sources) == 0


def test_cli_sources_command():
    result = runner.invoke(app, ["sources"])

    assert result.exit_code == 0
    assert "generator" in result.stdout
    assert "jsonl" in result.stdout
    assert "api-stub" in result.stdout


def test_cli_read_with_generator():
    result = runner.invoke(app, ["read", "--gen", "3"])

    assert result.exit_code == 0
    assert "ID: GEN-1" in result.stdout
    assert "Всего задач: 3" in result.stdout


def test_cli_read_no_sources_warning():
    result = runner.invoke(app, ["read"])

    assert result.exit_code == 0


def test_cli_read_file_not_found_error(tmp_path):
    fake_file = tmp_path / "i_dont_exist.jsonl"

    result = runner.invoke(app, ["read", "--jsonl", str(fake_file)])

    assert result.exit_code == 1
