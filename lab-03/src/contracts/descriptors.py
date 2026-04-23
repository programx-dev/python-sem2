from datetime import datetime
from enum import Enum
from typing import Any, Type


class TaskException(Exception):
    """Исключение для ошибок валидации данных задачи."""

    pass


class BaseDataDescriptor:
    """Базовый data-descriptor для исключения дублирования кода __set_name__ и __get__."""

    def __set_name__(self, owner: type, name: str):
        self.public_name = name
        self.private_name = f"_{name}"

    def __get__(self, instance: object | None, owner: type) -> Any:
        if instance is None:
            return self
        return getattr(instance, self.private_name, None)

    def __set__(self, instance: object, value: Any):
        raise NotImplementedError(
            "Метод __set__ должен быть переопределен в подклассах."
        )


class MetadataDescriptor:
    """
    Non-data descriptor.
    Демонстрирует различие: у него нет метода __set__.
    Используется для получения мета-информации о классе или объекте.
    """

    def __get__(self, instance: object | None, owner: type) -> str:
        if instance is None:
            return f"Metadata for class {owner.__name__}"
        return (
            f"Instance of {owner.__name__} (ID: {getattr(instance, '_id', 'Unknown')})"
        )


class NotEmptyStrDescriptor(BaseDataDescriptor):
    """Валидатор: только непустые строки."""

    def __set__(self, instance: object, value: str):
        if not isinstance(value, str) or not value.strip():
            raise TaskException(
                f"Ошибка в '{self.public_name}': ожидалась непустая строка."
            )
        setattr(instance, self.private_name, value.strip())


class PriorityDescriptor(BaseDataDescriptor):
    """Валидатор: целое число от 0 до 100."""

    def __set__(self, instance: object, value: int):
        if not isinstance(value, int):
            raise TaskException(
                f"Приоритет должен быть числом, а не {type(value).__name__}."
            )
        if not (0 <= value <= 100):
            raise TaskException("Приоритет должен быть в диапазоне от 0 до 100.")
        setattr(instance, self.private_name, value)


class EnumValidator(BaseDataDescriptor):
    """Валидатор для проверки принадлежности значения к конкретному Enum."""

    def __init__(self, enum_cls: Type[Enum]):
        self.enum_cls = enum_cls

    def __set__(self, instance: object, value: Enum):
        if not isinstance(value, self.enum_cls):
            raise TaskException(
                f"Значение '{value}' не является допустимым для {self.enum_cls.__name__}."
            )
        setattr(instance, self.private_name, value)


class DatetimeDescriptor(BaseDataDescriptor):
    """Валидатор даты. Поддерживает установку через строку или объект datetime."""

    def __init__(self, format_str: str = "%d.%m.%Y %H:%M:%S", read_only: bool = False):
        self.format_str = format_str
        self.read_only = read_only

    def __set__(self, instance: object, value: str | datetime):
        if self.read_only and hasattr(instance, self.private_name):
            raise TaskException(
                f"Поле '{self.public_name}' доступно только для чтения."
            )

        if isinstance(value, str):
            try:
                dt_value = datetime.strptime(value, self.format_str)
            except ValueError:
                raise TaskException(
                    f"Неверный формат даты для '{self.public_name}'. Ожидалось: {self.format_str}"
                )
        elif isinstance(value, datetime):
            dt_value = value
        else:
            raise TaskException(
                f"Для поля '{self.public_name}' ожидалась дата или строка."
            )

        setattr(instance, self.private_name, dt_value)
