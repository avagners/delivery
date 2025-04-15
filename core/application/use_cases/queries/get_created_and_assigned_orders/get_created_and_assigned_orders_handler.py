from sqlalchemy import text
from infrastructure.adapters.postgres.session_factory import create_session
from core.application.use_cases.queries.get_created_and_assigned_orders.get_created_and_assigned_orders_query import GetCreatedAndAssignedOrdersQuery
from core.application.use_cases.queries.get_created_and_assigned_orders.get_created_and_assigned_orders_response import GetCreatedAndAssignedOrdersResponse, OrderDTO, Location


class GetCreatedAndAssignedOrdersHandler:

    def handle(self, query: GetCreatedAndAssignedOrdersQuery) -> GetCreatedAndAssignedOrdersResponse:
        orders = []
        with create_session() as session:
            result = session.execute(
                text("""
                    SELECT id, location_x, location_y
                    FROM public.orders
                    WHERE status IN ('CREATED', 'ASSIGNED')
                """)
            ).fetchall()

            for row in result:
                order = OrderDTO(
                    id=row.id,
                    location=Location(x=row.location_x, y=row.location_y)
                )
                orders.append(order)

        return GetCreatedAndAssignedOrdersResponse(orders=orders)


if __name__ == "__main__":
    handler = GetCreatedAndAssignedOrdersHandler()
    query = GetCreatedAndAssignedOrdersQuery()
    response = handler.handle(query)

    if not response.orders:
        print("Нет активных заказов (Created / Assigned)!")
    else:
        print("Список активных заказов:")
        for order in response.orders:
            print(f"- ID: {order.id} | Location: ({order.location.x}, {order.location.y})")
