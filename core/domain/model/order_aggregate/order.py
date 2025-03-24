import uuid
from typing import Optional


from core.domain.model.shared_kernel.location import Location
from core.domain.model.order_aggregate.order_status import OrderStatus, OrderStatusValue
from core.domain.model.shared_kernel.aggregate import Aggregate


class Order(Aggregate):
    """Заказ"""

    def __init__(self, order_id: uuid.UUID, location: Location):
        if not order_id:
            raise ValueError("Order ID is required")
        if not location:
            raise ValueError("Location is required")

        super().__init__(order_id)
        self.location = location
        self.status = OrderStatus(OrderStatusValue.CREATED)
        self.courier_id: Optional[uuid.UUID] = None

    def assign_to_courier(self, courier_id: uuid.UUID):
        """Назначение заказа курьеру"""
        if not courier_id:
            raise ValueError("Courier ID is required")
        if self.status != OrderStatus(OrderStatusValue.CREATED):
            raise ValueError("Cannot assign an already assigned or completed order.")

        self.status = OrderStatus(OrderStatusValue.ASSIGNED)
        self.courier_id = courier_id

    def complete(self):
        """Завершение заказа"""
        if self.status != OrderStatus(OrderStatusValue.ASSIGNED):
            raise ValueError("Cannot complete an order that has not been assigned.")

        self.status = OrderStatus(OrderStatusValue.COMPLETED)
