from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class Task:
    """
    Представление единицы работы в системе.
    """

    id: str
    payload: Any
