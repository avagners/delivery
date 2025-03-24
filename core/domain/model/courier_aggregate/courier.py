import uuid

from core.domain.model.shared_kernel.location import Location
from core.domain.model.courier_aggregate.transport import Transport
from core.domain.model.courier_aggregate.courier_status import CourierStatus, CourierStatusValue
from core.domain.model.shared_kernel.aggregate import Aggregate
from core.domain.model.shared_kernel.business_rule_exception import BusinessRule


class Courier(Aggregate):
    """Курьер"""

    def __init__(self, name: str, transport_name: str, transport_speed: int, location: Location):
        self.check_rule(NotEmptyNameRule(name))
        self.check_rule(ValidLocationRule(location))

        super().__init__(uuid.uuid4())
        self.name = name
        self.transport = Transport(transport_name, transport_speed)
        self.location = location
        self.status = CourierStatus(CourierStatusValue.FREE)  # Курьер создается свободным

    def set_busy(self) -> None:
        """Установить статус 'занят'"""
        self.status = CourierStatus(CourierStatusValue.BUSY)

    def set_free(self) -> None:
        """Установить статус 'свободен'"""
        self.status = CourierStatus(CourierStatusValue.FREE)

    def calc_steps_to_location(self, target_location: Location) -> int:
        """Вычислить количество шагов до указанного местоположения"""
        if not isinstance(target_location, Location):
            raise ValueError("Target location must be a Location instance")

        distance = self.location.distance_to(target_location)
        steps = distance // self.transport.speed
        if distance % self.transport.speed != 0:
            steps += 1  # Округляем вверх, если остались неполные клетки

        return steps

    def move_towards(self, target_location: Location):
        """Переместиться на 1 шаг в сторону цели"""
        if not isinstance(target_location, Location):
            raise ValueError("Target location must be a Location instance")

        self.location = self.transport.move_towards(self.location, target_location)


class NotEmptyNameRule(BusinessRule):
    """Правило: имя курьера не может быть пустым"""

    def __init__(self, name: str):
        self.name = name

    def is_broken(self) -> bool:
        return not self.name.strip()

    def __str__(self):
        return "Courier name cannot be empty."


class ValidLocationRule(BusinessRule):
    """Правило: локация курьера должна быть корректной"""

    def __init__(self, location: Location):
        self.location = location

    def is_broken(self) -> bool:
        return not isinstance(self.location, Location)

    def __str__(self):
        return "Courier location must be a valid Location object."


if __name__ == "__main__":
    courier = Courier("Иван", "Велосипед", 2, Location(1, 1))
    target_loacation = Location(5, 5)
    print(courier.calc_steps_to_location(target_loacation))  # Выведет 4 шага
    courier.move_towards(target_loacation)  # Курьер делает шаг
    print(courier.location)  # Новая позиция после движения
