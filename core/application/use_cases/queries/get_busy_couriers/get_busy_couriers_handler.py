from sqlalchemy import text

from infrastructure.adapters.postgres.session_factory import create_session
from core.application.use_cases.queries.get_busy_couriers.get_busy_couriers_query import GetBusyCouriersQuery
from core.application.use_cases.queries.get_busy_couriers.get_busy_couriers_response import CourierDTO, Location, GetBusyCouriersResponse


class GetBusyCouriersHandler:

    def handle(self, query: GetBusyCouriersQuery) -> GetBusyCouriersResponse:

        couriers = []
        with create_session() as session:
            result = session.execute(
                text("""
                    SELECT id, name, location_x, location_y
                    FROM public.couriers
                    /* WHERE status = 'BUSY' */
                """)
            ).fetchall()

            for row in result:
                courier = CourierDTO(
                    id=row.id,
                    name=row.name,
                    location=Location(x=row.location_x, y=row.location_y)
                )
                couriers.append(courier)

        return GetBusyCouriersResponse(couriers=couriers)
