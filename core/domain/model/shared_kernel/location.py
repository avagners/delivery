from dataclasses import dataclass
import random
from enum import Enum


class ValueObject:
    """Базовый класс для всех Value-Object"""


class LocationSize(Enum):
    """Перечисление для минимального и максимального размера координат."""
    MIN = 1
    MAX = 10


@dataclass(frozen=True)
class Location(ValueObject):
    """Координата на доске."""
    x: int
    y: int

    def __post_init__(self):
        """Проверка значений координат после инициализации."""
        if not (LocationSize.MIN.value <= self.x <= LocationSize.MAX.value):
            raise ValueError(
                f"x must be between {LocationSize.MIN.value} and {LocationSize.MAX.value}"
            )
        if not (LocationSize.MIN.value <= self.y <= LocationSize.MAX.value):
            raise ValueError(
                f"y must be between {LocationSize.MIN.value} and {LocationSize.MAX.value}"
            )

    @classmethod
    def create_random_location(cls) -> "Location":
        """Создать случайный объект."""
        x = random.randint(LocationSize.MIN.value, LocationSize.MAX.value)
        y = random.randint(LocationSize.MIN.value, LocationSize.MAX.value)
        return cls(x, y)

    def distance_to(self, other: "Location") -> int:
        """Вычислить расстояние."""
        if not isinstance(other, Location):
            raise ValueError("Можно рассчитать расстояние только между двумя Location")
        return abs(self.x - other.x) + abs(self.y - other.y)
