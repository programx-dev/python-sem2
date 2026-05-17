from src.contracts.task_handler import TaskHandlerProtocol
from src.contracts.task_source import TaskSourceProtocol
from src.handlers import LoggingTaskHandler
from src.sources.generator import GeneratorSource


def test_generator_satisfies_async_source_protocol():
    """Проверка, что GeneratorSource соответствует асинхронному протоколу."""
    source = GeneratorSource(count=1)
    assert isinstance(source, TaskSourceProtocol)
    assert hasattr(source, "get_async_tasks")


def test_logging_handler_satisfies_protocol():
    """Проверка, что LoggingTaskHandler соответствует протоколу обработчика."""
    handler = LoggingTaskHandler()
    assert isinstance(handler, TaskHandlerProtocol)
    assert hasattr(handler, "handle")


def test_invalid_source_protocol_missing_method():
    """Проверка: если метода get_async_tasks нет, протокол не соблюден."""

    class NotASource:
        pass

    assert not isinstance(NotASource(), TaskSourceProtocol)


def test_invalid_handler_protocol_missing_method():
    """Проверка: если метода handle нет, объект не является хендлером."""

    class NoHandleMethod:
        def process(self, task):
            pass

    assert not isinstance(NoHandleMethod(), TaskHandlerProtocol)
