import pytest
from infrastructure.adapters.grpc.geo_service.geo_client import GeoClient


def test_should_return_location_for_valid_address(geo_client):
    # Arrange
    street_name = "Мобильная"

    # Act
    location = geo_client.get_location_by_street(street_name)

    # Assert
    assert location is not None
    assert location.x, int
    assert location.y, int
    assert location.x == 7
    assert location.y == 7


def test_should_raise_exception_for_invalid_address(geo_client):
    # Arrange
    street_name = ""  # Пустой адрес

    # Act + Assert
    with pytest.raises(Exception):
        geo_client.get_location_by_street(street_name)
