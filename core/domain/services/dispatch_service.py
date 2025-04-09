from abc import ABC, abstractmethod
from typing import List

from core.domain.model.courier_aggregate.courier import Courier
from core.domain.model.courier_aggregate.courier_status import CourierStatusValue
from core.domain.model.order_aggregate.order import Order
from core.domain.model.shared_kernel.location import Location


class ADispatchService(ABC):

    @abstractmethod
    def dispatch(self, order: Order, couriers: List[Courier]) -> Courier:
        pass


class DispatchService(ADispatchService):
    """Сервис для распределения заказов между курьерами"""

    @staticmethod
    def dispatch(order: Order, couriers: List[Courier]) -> Courier:
        """
        Выбирает наиболее подходящего курьера для заказа.

        Args:
            order: Заказ, который нужно распределить
            couriers: Список доступных курьеров

        Returns:
            Курьер, который быстрее всего сможет доставить заказ

        Raises:
            ValueError: Если нет доступных курьеров
        """
        # Фильтруем только свободных курьеров
        free_couriers = [c for c in couriers if c.status.name == CourierStatusValue.FREE]
        if not free_couriers:
            raise ValueError("No available couriers")

        # Для каждого курьера вычисляем время доставки (кол-во шагов)
        courier_distances = [
            (courier, courier.calc_steps_to_location(order.location))
            for courier in free_couriers
        ]

        # Выбираем курьера с минимальным расстоянием
        best_courier, _ = min(courier_distances, key=lambda x: x[1])

        return best_courier


if __name__ == "__main__":
    import uuid
    courier1 = Courier("Иван", "Велосипед", 2, Location(1, 1))
    courier2 = Courier("Иван2", "Велосипед2", 3, Location(1, 3))
    courier3 = Courier("Иван3", "Велосипед3", 1, Location(2, 3))

    couriers = [courier1, courier2, courier3]
    order = Order(uuid.uuid4(), Location(5, 5))

    best_courier = DispatchService.dispatch(order=order, couriers=couriers)
