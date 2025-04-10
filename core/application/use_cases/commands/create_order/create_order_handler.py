from dataclasses import dataclass

from core.domain.model.order_aggregate.order import Order
from core.domain.model.shared_kernel.location import Location
from core.application.use_cases.commands.create_order.create_order_command import CreateOrderCommand
from infrastructure.adapters.postgres.unit_of_work import UnitOfWork


@dataclass
class CreateOrderCommandHandler:
    unit_of_work: UnitOfWork

    def handle(self, massege: CreateOrderCommand) -> None:

        # Получаем геопозицию из Geo (пока ставим рандомное значение)
        location = Location.create_random_location()

        # Создаем заказ
        order = Order(
            order_id=massege.basket_id,  # ID заказа совпадает с ID корзины
            location=location
        )

        # Сохраняем
        with self.unit_of_work as uow:
            uow.orders.add(order)
