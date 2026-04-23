from typing import Callable

from src.contracts.task_source import TaskSource

SourceFactory = Callable[..., TaskSource]

REGISTRY: dict[str, SourceFactory] = {}


def register_source(name: str):
    """
    Декоратор для регистрации фабрики источника.
    """

    def _decorator(factory: SourceFactory):
        REGISTRY[name] = factory

        return factory

    return _decorator
