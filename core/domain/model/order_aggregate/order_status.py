from dataclasses import dataclass
from enum import Enum
from typing import Any

from core.domain.model.shared_kernel.value_object import ValueObject


class OrderStatusValue(Enum):
    """Статус заказа"""

    CREATED = "created"
    ASSIGNED = "assigned"
    COMPLETED = "completed"

    def __str__(self):
        return self.value


@dataclass(frozen=True)
class OrderStatus(ValueObject):
    """Value Object для статуса заказа"""

    name: OrderStatusValue

    @classmethod
    def set_created(cls) -> 'OrderStatus':
        return cls(OrderStatusValue.CREATED)

    @classmethod
    def set_assigned(cls) -> 'OrderStatus':
        return cls(OrderStatusValue.ASSIGNED)

    @classmethod
    def set_completed(cls) -> 'OrderStatus':
        return cls(OrderStatusValue.COMPLETED)

    def __post_init__(self):
        # Проверка, что значение статуса допустимо
        if self.name not in [status for status in OrderStatusValue]:
            raise ValueError(f"Invalid status: {self.name}")

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, OrderStatus):
            return False
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

    def __str__(self) -> str:
        return self.name.value
