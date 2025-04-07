from typing import Optional, List
import uuid

from core.domain.model.courier_aggregate.courier import Courier, CourierStatus, CourierStatusValue
from core.ports.сourier_repository_abc import CourierRepository


class InMemoryCourierRepository(CourierRepository):
    """Реализация репозитория курьеров в памяти"""

    def __init__(self):
        self._couriers = {}

    def add(self, courier: Courier) -> None:
        if courier.id in self._couriers:
            raise ValueError(f"Courier with id {courier.id} already exists")
        self._couriers[courier.id] = courier

    def update(self, courier: Courier) -> None:
        if courier.id not in self._couriers:
            raise ValueError(f"Courier with id {courier.id} not found")
        self._couriers[courier.id] = courier

    def get_by_id(self, courier_id: uuid.UUID) -> Optional[Courier]:
        return self._couriers.get(courier_id)

    def get_all_free(self) -> List[Courier]:
        return [
            courier for courier in self._couriers.values()
            if courier.status == CourierStatus(CourierStatusValue.FREE)
        ]
