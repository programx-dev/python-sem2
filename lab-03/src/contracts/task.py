from datetime import datetime, timedelta
from enum import Enum

from src.contracts.descriptors import (
    DatetimeDescriptor,
    EnumValidator,
    MetadataDescriptor,
    NotEmptyStrDescriptor,
    PriorityDescriptor,
    TaskException,
)


class TaskStatus(Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class Task:
    """
    Класс Модель задачи с инкапсуляцией и валидацией.
    """

    # --- Дескрипторы данных ---
    description: str = NotEmptyStrDescriptor()  # type: ignore
    priority: int = PriorityDescriptor()  # type: ignore
    status: Enum = EnumValidator(TaskStatus)  # type: ignore
    created_at: datetime = DatetimeDescriptor(read_only=True)  # type: ignore

    # --- Дескрипторы не данных ---
    field_info = MetadataDescriptor()

    def __init__(
        self,
        task_id: str,
        description: str,
        priority: int,
        status: TaskStatus,
        deadline: str | datetime,
        created_at: str | datetime | None = None,
    ):
        self.created_at = created_at or datetime.now()  # type: ignore
        self.description = description
        self.priority = priority
        self.status = status

        self._id = task_id
        self.deadline = deadline

    @property
    def id(self) -> str:
        """Публичный API для идентификатора (только для чтения)."""
        return self._id

    @property
    def deadline(self) -> datetime | None:
        return self._deadline

    @deadline.setter
    def deadline(self, value: str | datetime):
        """
        Срок не может быть раньше времени создания.
        """
        if isinstance(value, str):
            new_deadline = datetime.strptime(value, "%d.%m.%Y %H:%M:%S")
        elif isinstance(value, datetime):
            new_deadline = value
        else:
            raise TaskException("Ожидалась строка или datetime")

        if new_deadline < self.created_at:
            raise TaskException(
                "Срок не может быть в прошлом относительно даты создания."
            )

        self._deadline = new_deadline

    @property
    def is_overdue(self) -> bool:
        """Вычисляемое свойство: просрочена ли задача."""
        if self.deadline is None:
            return False

        return datetime.now() > self.deadline and self.status != TaskStatus.DONE

    @property
    def remaining_time(self) -> timedelta | None:
        """Вычисляемое свойство: сколько времени осталось."""
        if self.deadline is None:
            return None

        return self.deadline - datetime.now()

    def __repr__(self):
        return (
            f"Task(id='{self.id}', status={self.status.name}, priority={self.priority})"
        )
