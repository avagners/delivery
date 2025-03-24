from dataclasses import dataclass
from enum import Enum
from typing import Any

from core.domain.model.shared_kernel.value_object import ValueObject


class CourierStatusValue(Enum):
    """Статус курьера"""

    FREE = "free"
    BUSY = "busy"

    def __str__(self):
        return self.value


@dataclass(frozen=True)
class CourierStatus(ValueObject):
    """Value Object для статуса курьера"""

    name: str

    def __post_init__(self):
        # Проверка, что значение статуса допустимо
        if self.name not in [status.value for status in CourierStatusValue]:
            raise ValueError(f"Invalid status: {self.name}")

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, CourierStatus):
            return False
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

    def __str__(self) -> str:
        return self.name
