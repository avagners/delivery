# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from typing import Any, List
from api.adapters.http.contract.src.api.models.courier import Courier
from api.adapters.http.contract.src.api.models.error import Error
from api.adapters.http.contract.src.api.models.order import Order


class BaseDefaultApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseDefaultApi.subclasses = BaseDefaultApi.subclasses + (cls,)
    def create_order(
        self,
    ) -> None:
        """Позволяет создать заказ с целью тестирования"""
        ...


    def get_couriers(
        self,
    ) -> List[Courier]:
        """Позволяет получить всех курьеров"""
        ...


    def get_orders(
        self,
    ) -> List[Order]:
        """Позволяет получить все незавершенные"""
        ...
