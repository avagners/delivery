from dataclasses import dataclass

from core.application.use_cases.commands.move_couriers.move_couriers_command import MoveCouriersCommand
from infrastructure.adapters.postgres.unit_of_work import UnitOfWork


@dataclass
class MoveCouriersCommandHandler:
    unit_of_work: UnitOfWork

    def handle(self, message: MoveCouriersCommand) -> None:

        with self.unit_of_work as uow:
            # Восстанавливаем агрегаты
            assigned_orders = uow.orders.get_all_assigned()
            if not assigned_orders:
                return

            # Изменяем агрегаты
            for order in assigned_orders:
                if order.courier_id is None:
                    raise ValueError(f"No courier found for order {order.id}")

                courier = uow.couriers.get_by_id(order.courier_id)

                courier.move_towards(order.location)
                if courier.location == order.location:
                    order.complete()
                    courier.set_free()

                # Сохраняем
                uow.couriers.update(courier)
                uow.orders.update(order)
