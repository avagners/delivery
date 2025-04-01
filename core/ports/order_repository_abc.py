from abc import ABC, abstractmethod
from typing import Iterable, Optional
from uuid import UUID

from core.domain.model.order_aggregate.order import Order


class OrderRepository(ABC):
    """Абстрактный репозиторий для работы с заказами"""

    @abstractmethod
    def add(self, order: Order) -> None:
        """Добавить новый заказ в репозиторий.

        Args:
            order: Заказ для добавления

        Raises:
            ValueError: Если заказ с таким ID уже существует
        """
        pass

    @abstractmethod
    def update(self, order: Order) -> None:
        """Обновить существующий заказ в репозитории.

        Args:
            order: Заказ с обновленными данными

        Raises:
            ValueError: Если заказ с таким ID не найден
        """
        pass

    @abstractmethod
    def get_by_id(self, order_id: UUID) -> Optional[Order]:
        """Получить заказ по его идентификатору.

        Args:
            order_id: UUID идентификатор заказа

        Returns:
            Найденный заказ или None, если заказ не существует
        """
        pass

    @abstractmethod
    def get_one_created(self) -> Optional[Order]:
        """Получить один любой заказ со статусом 'Created'.

        Returns:
            Первый найденный заказ со статусом Created или None,
            если таких заказов нет
        """
        pass

    @abstractmethod
    def get_all_assigned(self) -> Iterable[Order]:
        """Получить все заказы со статусом 'Assigned'.

        Returns:
            Итерируемый объект всех заказов со статусом 'Assigned'
            (может быть пустым)
        """
        pass
