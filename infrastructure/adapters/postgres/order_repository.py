from uuid import UUID
from typing import Iterable, Optional
from sqlalchemy.orm import Session

from core.domain.model.order_aggregate.order import Order, OrderStatusValue, OrderStatus
from core.domain.model.shared_kernel.location import Location
from core.ports.order_repository_abc import OrderRepository
from infrastructure.adapters.postgres.models import OrderModel


class OrderRepositoryImpl(OrderRepository):
    """Реализация репозитория заказов с использованием SQLAlchemy"""

    def __init__(self, session: Session):
        self.session = session

    def add(self, order: Order) -> None:
        if self.get_by_id(order.id) is not None:
            raise ValueError(f"Order with id {order.id} already exists")

        order_model = OrderModel(
            id=order.id,
            location_x=order.location.x,
            location_y=order.location.y,
            status=OrderStatusValue(order.status.name.value),
            courier_id=order.courier_id
        )
        self.session.add(order_model)

    def update(self, order: Order) -> None:
        order_model = self.session.get(OrderModel, order.id)
        if order_model is None:
            raise ValueError(f"Order with id {order.id} not found")

        order_model.location_x = order.location.x
        order_model.location_y = order.location.y
        order_model.status = order.status.name
        order_model.courier_id = order.courier_id

    def get_by_id(self, order_id: UUID) -> Optional[Order]:
        order_model = self.session.get(OrderModel, order_id)
        if order_model is None:
            return None

        return self._to_domain(order_model)

    def get_one_created(self) -> Optional[Order]:
        order_model = self.session.query(OrderModel).filter(
            OrderModel.status == OrderStatusValue.CREATED
        ).first()
        return self._to_domain(order_model) if order_model else None

    def get_all_assigned(self) -> Iterable[Order]:
        query = self.session.query(OrderModel).filter(
            OrderModel.status == OrderStatusValue.ASSIGNED
        )
        return [self._to_domain(model) for model in query.all()]

    def _to_domain(self, model: OrderModel) -> Order:
        order = Order(
            order_id=model.id,
            location=Location(int(model.location_x), int(model.location_y))
        )
        order.status = OrderStatus(OrderStatusValue(model.status))
        order.courier_id = model.courier_id
        return order
