from abc import ABC, abstractmethod
from typing import Iterable, Optional
from uuid import UUID

from core.domain.model.courier_aggregate.courier import Courier


class CourierRepository(ABC):
    """Абстрактный репозиторий для работы с курьерами"""

    @abstractmethod
    def add(self, courier: Courier) -> None:
        """Добавить нового курьера в репозиторий.

        Args:
            courier: Курьер для добавления

        Raises:
            ValueError: Если курьер с таким ID уже существует
        """
        pass

    @abstractmethod
    def update(self, courier: Courier) -> None:
        """Обновить существующего курьера в репозитории.

        Args:
            courier: Курьер с обновленными данными

        Raises:
            ValueError: Если курьер с таким ID не найден
        """
        pass

    @abstractmethod
    def get_by_id(self, courier_id: UUID) -> Optional[Courier]:
        """Получить курьера по его идентификатору.

        Args:
            courier_id: UUID идентификатор курьера

        Returns:
            Найденный курьер или None, если курьер не существует
        """
        pass

    @abstractmethod
    def get_all_free(self) -> Iterable[Courier]:
        """Получить всех курьеров со статусом 'Free'.

        Returns:
            Список всех свободных курьеров (может быть пустым)
        """
        pass
