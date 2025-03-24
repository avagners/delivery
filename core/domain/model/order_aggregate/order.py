import uuid
from typing import Optional

from core.domain.model.shared_kernel.location import Location
from core.domain.model.order_aggregate.order_status import OrderStatus, OrderStatusValue
from core.domain.model.shared_kernel.aggregate import Aggregate
from core.domain.model.shared_kernel.business_rule_exception import BusinessRule


class Order(Aggregate):
    """Заказ"""

    def __init__(self, order_id: uuid.UUID, location: Location):
        super().__init__(order_id)

        # Проверка бизнес-правил
        self.check_rule(ValidOrderIdRule(order_id))
        self.check_rule(ValidLocationRule(location))

        self.location = location
        self.status = OrderStatus(OrderStatusValue.CREATED)
        self.courier_id: Optional[uuid.UUID] = None

    def assign_to_courier(self, courier_id: uuid.UUID):
        """Назначение заказа курьеру"""
        if not courier_id:
            raise ValueError("Courier ID is required")

        self.check_rule(OrderCanBeAssignedRule(self.status))

        self.status = OrderStatus(OrderStatusValue.ASSIGNED)
        self.courier_id = courier_id

    def complete(self):
        """Завершение заказа"""
        self.check_rule(OrderCanBeCompletedRule(self.status))

        self.status = OrderStatus(OrderStatusValue.COMPLETED)


# Бизнес-правила для Order
class ValidOrderIdRule(BusinessRule):
    """Правило: ID заказа должен быть валидным"""

    def __init__(self, order_id: uuid.UUID):
        self.order_id = order_id

    def is_broken(self) -> bool:
        return self.order_id is None or self.order_id == uuid.UUID(int=0)

    def __str__(self):
        return "Order ID cannot be empty or zero."


class ValidLocationRule(BusinessRule):
    """Правило: местоположение заказа должно быть задано"""

    def __init__(self, location: Location):
        self.location = location

    def is_broken(self) -> bool:
        return self.location is None

    def __str__(self):
        return "Order location cannot be empty."


class OrderCanBeAssignedRule(BusinessRule):
    """Правило: заказ можно назначить только если он в статусе 'CREATED'"""

    def __init__(self, status: OrderStatus):
        self.status = status

    def is_broken(self) -> bool:
        return self.status != OrderStatus(OrderStatusValue.CREATED)

    def __str__(self):
        return "Order can only be assigned if it is in 'CREATED' status."


class OrderCanBeCompletedRule(BusinessRule):
    """Правило: заказ можно завершить только если он в статусе 'ASSIGNED'"""

    def __init__(self, status: OrderStatus):
        self.status = status

    def is_broken(self) -> bool:
        return self.status != OrderStatus(OrderStatusValue.ASSIGNED)

    def __str__(self):
        return "Order can only be completed if it is in 'ASSIGNED' status."


if __name__ == "__main__":
    # Создание заказа
    order_id = uuid.uuid4()
    location = Location(5, 10)
    order = Order(order_id, location)

    print(f"Создан заказ: ID={order.id}, Статус={order.status.name}, Локация=({order.location.x}, {order.location.y})")

    # Назначение курьера
    courier_id = uuid.uuid4()
    try:
        order.assign_to_courier(courier_id)
        print(f"Заказ {order.id} назначен курьеру {order.courier_id}, новый статус: {order.status.name}")
    except Exception as e:
        print(f"Ошибка при назначении курьера: {e}")

    # Завершение заказа
    try:
        order.complete()
        print(f"Заказ {order.id} завершён, новый статус: {order.status.name}")
    except Exception as e:
        print(f"Ошибка при завершении заказа: {e}")
