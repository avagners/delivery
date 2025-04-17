from abc import ABC, abstractmethod

from core.domain.model.shared_kernel.location import Location


class LocationProvider(ABC):
    @abstractmethod
    def get_location_by_street(self, street: str) -> Location:
        """
        Получить геокоординаты по названию улицы.

        :param street: Название улицы.
        :return: Location — объект с координатами.
        """
        pass
