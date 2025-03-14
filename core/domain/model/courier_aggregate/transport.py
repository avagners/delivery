from dataclasses import dataclass, field
import uuid
from abc import ABC, abstractmethod

from core.domain.model.shared_kernel.location import Location


class BusinessRule(ABC):
    """Абстрактный класс для бизнес-правил"""

    @abstractmethod
    def is_broken(self) -> bool:
        """Проверяет, нарушено ли правило"""
        raise NotImplementedError


class BusinessRuleBrokenException(Exception):
    """Исключение, которое выбрасывается при нарушении бизнес-правила"""

    def __init__(self, rule: BusinessRule):
        self.rule = rule
        super().__init__(f"Business rule {rule.__class__.__name__} is broken: {rule}")


@dataclass
class Entity:
    """Базовый класс для всех Entities"""
    id: uuid.UUID = field(default_factory=lambda: globals()['Entity'].next_id(), kw_only=True)

    @classmethod
    def next_id(cls) -> uuid.UUID:
        """Генерирует новый UUID"""
        return uuid.uuid4()

    def check_rule(self, rule: BusinessRule):
        """Проверяет, нарушено ли бизнес-правило. Если нарушено, выбрасывает исключение."""
        if rule.is_broken():
            raise BusinessRuleBrokenException(rule)

    def __eq__(self, other) -> bool:
        """Сравнивает две Entity по их идентификатору"""
        if not isinstance(other, Entity):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """Возвращает хэш Entity на основе её идентификатора"""
        return hash(self.id)


@dataclass
class Transport(Entity):
    """Транспорт курьера"""
    name: str
    speed: int

    def __post_init__(self):
        # Проверка бизнес-правил при создании объекта
        self.check_rule(NotEmptyNameRule(self.name))
        self.check_rule(ValidSpeedRule(self.speed))

    def move_towards(self, current_location: Location, target_location: Location) -> Location:
        """
        Перемещает транспорт на один шаг в сторону целевого Location.
        Возвращает новый Location после перемещения.
        Транспорт может двигаться только по горизонтали или по вертикали за один шаг.
        """
        if current_location == target_location:
            return current_location  # Уже на месте

        # Вычисляем разницу по X и Y
        delta_x = target_location.x - current_location.x
        delta_y = target_location.y - current_location.y

        # Определяем, по какой оси двигаться (горизонталь или вертикаль)
        if abs(delta_x) >= abs(delta_y):
            # Двигаемся по горизонтали
            step_x = min(abs(delta_x), self.speed) * (1 if delta_x > 0 else -1)
            new_x = current_location.x + step_x
            new_y = current_location.y
        else:
            # Двигаемся по вертикали
            step_y = min(abs(delta_y), self.speed) * (1 if delta_y > 0 else -1)
            new_x = current_location.x
            new_y = current_location.y + step_y

        return Location(new_x, new_y)


# Бизнес-правила для Transport
class NotEmptyNameRule(BusinessRule):
    """Правило: название транспорта не может быть пустым"""

    def __init__(self, name: str):
        self.name = name

    def is_broken(self) -> bool:
        return not self.name.strip()

    def __str__(self):
        return "Name cannot be empty"


class ValidSpeedRule(BusinessRule):
    """Правило: скорость транспорта должна быть от 1 до 3"""

    def __init__(self, speed: int):
        self.speed = speed

    def is_broken(self) -> bool:
        return self.speed < 1 or self.speed > 3

    def __str__(self):
        return f"Speed must be between 1 and 3, but got {self.speed}"
