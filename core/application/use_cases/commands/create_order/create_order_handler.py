from dataclasses import dataclass

from core.domain.model.order_aggregate.order import Order
from core.domain.model.shared_kernel.location import Location
from core.application.use_cases.commands.create_order.create_order_command import CreateOrderCommand
from infrastructure.adapters.grpc.geo_service.geo_client import GeoClient
from infrastructure.adapters.postgres.unit_of_work import UnitOfWork


@dataclass
class CreateOrderCommandHandler:
    unit_of_work: UnitOfWork
    geo_client: GeoClient

    def handle(self, message: CreateOrderCommand) -> None:

        # Получаем координаты через сервис Geo
        location: Location = self.geo_client.get_location_by_street(message.street)

        # Создаем заказ
        order = Order(
            order_id=message.basket_id,  # ID заказа совпадает с ID корзины
            location=location
        )

        # Сохраняем
        with self.unit_of_work as uow:
            uow.orders.add(order)
