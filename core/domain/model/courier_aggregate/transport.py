from dataclasses import dataclass

from core.domain.model.shared_kernel.entity import Entity
from core.domain.model.shared_kernel.location import Location
from core.domain.model.shared_kernel.business_rule_exception import BusinessRule


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
