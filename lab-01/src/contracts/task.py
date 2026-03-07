from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class Task:
    """
    Объект-задача.
    """

    id: str
    payload: Any
