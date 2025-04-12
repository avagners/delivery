import uuid

from core.domain.model.shared_kernel.location import Location
from core.domain.model.order_aggregate.order import Order
from core.domain.model.order_aggregate.order_status import OrderStatusValue
from core.domain.model.courier_aggregate.courier import Courier
from core.domain.model.courier_aggregate.courier_status import CourierStatusValue 
from core.application.use_cases.commands.assign_orders.assign_orders_command import AssignOrdersCommand
from core.application.use_cases.commands.assign_orders.assign_orders_handler import AssignOrdersCommandHandler
from core.domain.services.dispatch_service import DispatchService


def test_assign_orders_command_handler(uow):
    # Arrange
    order_id = uuid.uuid4()
    print(order_id)

    order = Order(order_id=order_id, location=Location(10, 10))
    courier = Courier(
        name='Mike',
        transport_name='Bike',
        transport_speed=2,
        location=Location(1, 1)
    )

    with uow as setup_uow:
        setup_uow.orders.add(order)
        setup_uow.couriers.add(courier)

    handler = AssignOrdersCommandHandler(
        unit_of_work=uow,
        dispatch_service=DispatchService()
    )

    # Act
    handler.handle(AssignOrdersCommand())

    # Assert
    with uow as check_uow:
        updated_order = check_uow.orders.get_by_id(order_id)
        updated_courier = check_uow.couriers.get_by_id(courier.id)

        assert updated_order.status.name == OrderStatusValue.ASSIGNED
        assert updated_order.courier_id == courier.id

        assert updated_courier.status.name == CourierStatusValue.BUSY
