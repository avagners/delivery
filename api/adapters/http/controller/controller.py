import uuid

from config import DATABASE_URL
from api.adapters.http.contract.src.api.apis.default_api_base import BaseDefaultApi
from api.adapters.http.contract.src.api.models.order import Order
from api.adapters.http.contract.src.api.models.courier import Courier
from core.application.use_cases.commands.create_order.create_order_command import CreateOrderCommand
from core.application.use_cases.commands.create_order.create_order_handler import CreateOrderCommandHandler
from core.application.use_cases.queries.get_busy_couriers.get_busy_couriers_handler import GetBusyCouriersHandler
from core.application.use_cases.queries.get_busy_couriers.get_busy_couriers_query import GetBusyCouriersQuery
from core.application.use_cases.queries.get_created_and_assigned_orders.get_created_and_assigned_orders_handler import GetCreatedAndAssignedOrdersHandler
from core.application.use_cases.queries.get_created_and_assigned_orders.get_created_and_assigned_orders_query import GetCreatedAndAssignedOrdersQuery
from infrastructure.adapters.postgres.unit_of_work import UnitOfWork
from infrastructure.adapters.grpc.geo_service.geo_client import GeoClient


class Router(BaseDefaultApi):

    def get_orders(self):
        handler = GetCreatedAndAssignedOrdersHandler()
        response = handler.handle(query=GetCreatedAndAssignedOrdersQuery)  # запрос без параметров
        return [
            Order(
                id=str(order.id),
                location={"x": order.location.x, "y": order.location.y}
            )
            for order in response.orders
        ]

    def get_couriers(self):
        handler = GetBusyCouriersHandler()
        response = handler.handle(query=GetBusyCouriersQuery)
        return [
            Courier(
                id=str(courier.id),
                name=courier.name,
                location={"x": courier.location.x, "y": courier.location.y}
            )
            for courier in response.couriers
        ]

    def create_order(self):
        # Создаем команду (пока так)
        command = CreateOrderCommand(
            basket_id=uuid.uuid4(),
            street="Мобильная"
        )

        # Создаем handler с UoW
        handler = CreateOrderCommandHandler(unit_of_work=UnitOfWork(DATABASE_URL), geo_client=GeoClient())

        # Выполняем бизнес-логику
        handler.handle(command)

        return {
            "order": command.basket_id,
            "status": "created"
            }
