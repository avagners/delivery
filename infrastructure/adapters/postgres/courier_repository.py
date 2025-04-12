from uuid import UUID
from typing import Iterable, Optional
from sqlalchemy.orm import Session

from core.domain.model.courier_aggregate.courier import Courier
from core.domain.model.courier_aggregate.courier_status import CourierStatus, CourierStatusValue
from core.domain.model.shared_kernel.location import Location
from core.ports.courier_repository_abc import CourierRepository
from infrastructure.adapters.postgres.models import CourierModel


class CourierRepositoryImpl(CourierRepository):
    """Реализация репозитория курьеров с использованием SQLAlchemy"""

    def __init__(self, session: Session):
        self.session = session

    def add(self, courier: Courier) -> None:
        if self.get_by_id(courier.id) is not None:
            raise ValueError(f"Courier with id {courier.id} already exists")

        courier_model = CourierModel(
            id=courier.id,
            name=courier.name,
            transport_name=courier.transport.name,
            transport_speed=courier.transport.speed,
            location_x=courier.location.x,
            location_y=courier.location.y,
            status=CourierStatusValue(courier.status.name.value)
        )
        self.session.add(courier_model)

    def update(self, courier: Courier) -> None:
        courier_model = self.session.get(CourierModel, courier.id)
        if courier_model is None:
            raise ValueError(f"Courier with id {courier.id} not found")

        courier_model.name = courier.name
        courier_model.transport_name = courier.transport.name
        courier_model.transport_speed = courier.transport.speed
        courier_model.location_x = courier.location.x
        courier_model.location_y = courier.location.y
        courier_model.status = CourierStatusValue(courier.status.name.value)

    def get_by_id(self, courier_id: UUID) -> Optional[Courier]:
        courier_model = self.session.get(CourierModel, courier_id)
        if courier_model is None:
            return None

        return self._to_domain(courier_model)

    def get_all_free(self) -> Iterable[Courier]:
        query = self.session.query(CourierModel).filter(
            CourierModel.status == CourierStatusValue.FREE
        )
        return [self._to_domain(model) for model in query.all()]

    def get_all(self) -> Iterable[Courier]:
        query = self.session.query(CourierModel)
        return [self._to_domain(model) for model in query.all()]

    def _to_domain(self, model: CourierModel) -> Courier:
        courier = Courier(
            name=str(model.name),
            transport_name=str(model.transport_name),
            transport_speed=int(model.transport_speed),
            location=Location(int(model.location_x), int(model.location_y)),
            id=model.id
        )
        # Явно устанавливаем статус из БД
        courier.status = CourierStatus(CourierStatusValue(model.status))
        return courier
