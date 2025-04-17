import uuid
from core.application.use_cases.commands.create_order.create_order_command import CreateOrderCommand
from core.application.use_cases.commands.create_order.create_order_handler import CreateOrderCommandHandler
from infrastructure.adapters.postgres.unit_of_work import UnitOfWork
from infrastructure.adapters.grpc.geo_service.geo_client import GeoClient


def test_create_order_saved_in_db(uow: UnitOfWork, geo_client: GeoClient):
    handler = CreateOrderCommandHandler(unit_of_work=uow, geo_client=geo_client)

    basket_id = uuid.uuid4()
    command = CreateOrderCommand(
        basket_id=basket_id,
        street="Ленина, 1"
    )

    handler.handle(command)

    # Проверим, что заказ действительно записан в БД
    with uow as u:
        order = u.orders.get_by_id(basket_id)
        assert order is not None
        assert order.id == basket_id
