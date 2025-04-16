# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from api.adapters.http.contract.src.api.apis.default_api_base import BaseDefaultApi
import api.adapters.http.contract.src.openapi_server.impl

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    HTTPException,
    Path,
    Query,
    Response,
    Security,
    status,
)

from api.adapters.http.contract.src.api.models.extra_models import TokenModel  # noqa: F401
from typing import Any, List
from api.adapters.http.contract.src.api.models.courier import Courier
from api.adapters.http.contract.src.api.models.error import Error
from api.adapters.http.contract.src.api.models.order import Order


router = APIRouter()

ns_pkg = api.adapters.http.contract.src.openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/api/v1/orders",
    responses={
        201: {"description": "Успешный ответ"},
        200: {"model": Error, "description": "Ошибка"},
    },
    tags=["default"],
    summary="Создать заказ",
    response_model_by_alias=True,
)
def create_order(
) -> None:
    """Позволяет создать заказ с целью тестирования"""
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return BaseDefaultApi.subclasses[0]().create_order()


@router.get(
    "/api/v1/couriers",
    responses={
        200: {"model": List[Courier], "description": "Успешный ответ"},
        200: {"model": Error, "description": "Ошибка"},
    },
    tags=["default"],
    summary="Получить всех курьеров",
    response_model_by_alias=True,
)
def get_couriers(
) -> List[Courier]:
    """Позволяет получить всех курьеров"""
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return BaseDefaultApi.subclasses[0]().get_couriers()


@router.get(
    "/api/v1/orders/active",
    responses={
        200: {"model": List[Order], "description": "Успешный ответ"},
        200: {"model": Error, "description": "Ошибка"},
    },
    tags=["default"],
    summary="Получить все незавершенные заказы",
    response_model_by_alias=True,
)
def get_orders(
) -> List[Order]:
    """Позволяет получить все незавершенные"""
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return BaseDefaultApi.subclasses[0]().get_orders()
