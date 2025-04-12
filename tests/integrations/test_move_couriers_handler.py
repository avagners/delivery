import uuid

from core.application.use_cases.commands.move_couriers.move_couriers_command import MoveCouriersCommand
from core.application.use_cases.commands.move_couriers.move_couriers_handler import MoveCouriersCommandHandler
from core.application.use_cases.commands.assign_orders.assign_orders_command import AssignOrdersCommand
from core.application.use_cases.commands.assign_orders.assign_orders_handler import AssignOrdersCommandHandler
from core.domain.services.dispatch_service import DispatchService
from core.domain.model.courier_aggregate.courier import Courier
from core.domain.model.courier_aggregate.courier_status import CourierStatusValue
from core.domain.model.order_aggregate.order import Order
from core.domain.model.order_aggregate.order_status import OrderStatusValue
from core.domain.model.shared_kernel.location import Location


def test_move_couriers_command_handler(uow):
    # Arrange — добавляем курьеров и заказы в БД
    start_location = Location(1, 1)
    courier = Courier(
        name='Mike',
        transport_name='Bike',
        transport_speed=2,
        location=start_location
    )

    order_id = uuid.uuid4()
    order = Order(
        order_id=order_id,
        location=Location(1, 5),
    )

    with uow as u:
        u.couriers.add(courier)
        u.orders.add(order)

    handler_assign_orders = AssignOrdersCommandHandler(
        unit_of_work=uow,
        dispatch_service=DispatchService()
    )
    handler_assign_orders.handle(AssignOrdersCommand())

    # Act — выполняем команду "движения" курьеров
    handler = MoveCouriersCommandHandler(unit_of_work=uow)
    handler.handle(MoveCouriersCommand())

    # Assert — проверяем, что курьер сдвинулся и состояние заказа изменилось если достиг точки
    with uow as u:
        updated_order = u.orders.get_by_id(order_id)
        updated_courier = u.couriers.get_by_id(courier.id)

        # Курьер не достиг заказа. Он должен быть в новом положении и всё ещё занят
        assert updated_courier.location != updated_order.location
        assert updated_courier.location != start_location
        assert updated_courier.status.name == CourierStatusValue.BUSY
        assert updated_order.status.name == OrderStatusValue.ASSIGNED

    # Act — выполняем команду "движения" курьеров еще раз
    handler.handle(MoveCouriersCommand())

    # Assert — проверяем, что курьер сдвинулся и состояние заказа изменилось если достиг точки
    with uow as u:
        updated_order = u.orders.get_by_id(order_id)
        updated_courier = u.couriers.get_by_id(courier.id)

        # Курьер добрался до заказа, заказ должен быть завершён и статус курьера свободным
        assert updated_order.location == updated_courier.location
        assert updated_order.status.name == OrderStatusValue.COMPLETED
        assert updated_courier.status.name == CourierStatusValue.FREE
