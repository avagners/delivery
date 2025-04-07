from typing import Optional, List
import uuid

from core.domain.model.order_aggregate.order import Order, OrderStatus, OrderStatusValue
from core.ports.order_repository_abc import OrderRepository


class InMemoryOrderRepository(OrderRepository):
    """Реализация репозитория заказов в памяти"""

    def __init__(self):
        self._orders = {}

    def add(self, order: Order) -> None:
        if order.id in self._orders:
            raise ValueError(f"Order with id {order.id} already exists")
        self._orders[order.id] = order

    def update(self, order: Order) -> None:
        if order.id not in self._orders:
            raise ValueError(f"Order with id {order.id} not found")
        self._orders[order.id] = order

    def get_by_id(self, order_id: uuid.UUID) -> Optional[Order]:
        return self._orders.get(order_id)

    def get_one_created(self) -> Optional[Order]:
        for order in self._orders.values():
            if order.status == OrderStatus(OrderStatusValue.CREATED):
                return order
        return None

    def get_all_assigned(self) -> List[Order]:
        return [
            order for order in self._orders.values()
            if order.status == OrderStatus(OrderStatusValue.ASSIGNED)
        ]
