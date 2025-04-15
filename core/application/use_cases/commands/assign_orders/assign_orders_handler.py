from dataclasses import dataclass

from core.application.use_cases.commands.assign_orders.assign_orders_command import AssignOrdersCommand
from infrastructure.adapters.postgres.unit_of_work import UnitOfWork
from core.domain.services.dispatch_service import DispatchService


@dataclass
class AssignOrdersCommandHandler:
    unit_of_work: UnitOfWork
    dispatch_service: DispatchService

    def handle(self, command: AssignOrdersCommand) -> None:
        with self.unit_of_work as uow:
            # Получаем первый заказ в статусе Created
            order = uow.orders.get_one_created()
            if order is None:
                raise ValueError("Нет доступных заказов")

            # Получаем всех свободных курьеров
            free_couriers = uow.couriers.get_all_free()
            if not free_couriers:
                raise ValueError("Нет доступных курьеров")

            # Вызываем скоринг
            best_courier = self.dispatch_service.dispatch(order, free_couriers)
            # Назначаяем заказ на курьера и меняем статус курьера
            order.assign_to_courier(best_courier.id)
            best_courier.set_busy()

            # Назначаем заказ и обновляем БД
            uow.orders.update(order)
            uow.couriers.update(best_courier)
