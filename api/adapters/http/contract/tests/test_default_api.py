# coding: utf-8

from fastapi.testclient import TestClient


# from typing import Any, List  # noqa: F401
# from api.adapters.http.contract.src.api.models.courier import Courier  # noqa: F401
# from api.adapters.http.contract.src.api.models.error import Error  # noqa: F401
# from api.adapters.http.contract.src.api.models.order import Order  # noqa: F401


def test_create_order(client: TestClient):
    """Test case for create_order

    Создать заказ
    """

    headers = {
    }
    # uncomment below to make a request
    response = client.request(
       "POST",
       "/api/v1/orders",
       headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    assert response.status_code == 200


def test_get_couriers(client: TestClient):
    """Test case for get_couriers

    Получить всех курьеров
    """

    headers = {
    }
    # uncomment below to make a request
    response = client.request(
       "GET",
       "/api/v1/couriers",
       headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    assert response.status_code == 200


def test_get_orders(client: TestClient):
    """Test case for get_orders

    Получить все незавершенные заказы
    """

    headers = {
    }
    # uncomment below to make a request
    response = client.request(
       "GET",
       "/api/v1/orders/active",
       headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    assert response.status_code == 200
