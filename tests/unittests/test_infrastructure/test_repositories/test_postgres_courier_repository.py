import unittest
import uuid
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from core.domain.model.courier_aggregate.courier import Courier
from core.domain.model.courier_aggregate.courier_status import CourierStatusValue
from core.domain.model.shared_kernel.location import Location
from infrastructure.adapters.postgres.courier_repository import CourierRepositoryImpl
from infrastructure.adapters.postgres.models import CourierModel


class TestCourierRepository(unittest.TestCase):
    def setUp(self):
        self.mock_session = MagicMock(spec=Session)
        self.repo = CourierRepositoryImpl(self.mock_session)
        self.sample_courier = Courier(
            "Test Courier",
            "Bike",
            2,
            Location(1, 1)
        )

    def test_add_courier(self):
        # Настраиваем mock для get_by_id (должен возвращать None при первом вызове)
        self.mock_session.query.return_value.get.return_value = None

        # Вызываем тестируемый метод
        self.repo.add(self.sample_courier)

        # Проверяем что session.add был вызван с правильными аргументами
        self.mock_session.add.assert_called_once()

        # Получаем переданный в add аргумент
        args, _ = self.mock_session.add.call_args
        courier_model = args[0]

        # Проверяем корректность преобразования
        self.assertIsInstance(courier_model, CourierModel)
        self.assertEqual(courier_model.name, "Test Courier")
        self.assertEqual(courier_model.transport_speed, 2)
        self.assertEqual(courier_model.status, CourierStatusValue.FREE)

    def test_get_by_id_found(self):
        mock_model = CourierModel(
            id=self.sample_courier.id,
            name="Test Courier",
            transport_name="Bike",
            transport_speed=2,
            location_x=1,
            location_y=1,
            status="free"
        )

        self.mock_session.query.return_value.get.return_value = mock_model

        result = self.repo.get_by_id(self.sample_courier.id)

        self.assertIsNotNone(result)
        self.assertEqual(result.id, self.sample_courier.id)
        self.assertEqual(result.name, "Test Courier")

    def test_get_by_id_not_found(self):
        self.mock_session.query.return_value.get.return_value = None

        result = self.repo.get_by_id(uuid.uuid4())
        self.assertIsNone(result)

    def test_update_courier(self):
        mock_model = CourierModel(
            id=self.sample_courier.id,
            name="Old Name",
            transport_name="Bike",
            transport_speed=1,
            location_x=0,
            location_y=0,
            status="free"
        )

        self.mock_session.query.return_value.get.return_value = mock_model

        updated_courier = Courier(
            "Updated Name",
            "Car",
            3,
            Location(5, 5),
            id=self.sample_courier.id
        )
        updated_courier.set_busy()

        self.repo.update(updated_courier)

        self.assertEqual(mock_model.name, "Updated Name")
        self.assertEqual(mock_model.transport_speed, 3)
        self.assertEqual(mock_model.status, CourierStatusValue.BUSY)

    def test_get_all_free(self):
        mock_model = CourierModel(
            id=self.sample_courier.id,
            name="Free Courier",
            transport_name="Bike",
            transport_speed=2,
            location_x=1,
            location_y=1,
            status="free"
        )

        self.mock_session.query.return_value.filter.return_value.all.return_value = [mock_model]

        result = list(self.repo.get_all_free())

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].status.name.value, "free")


if __name__ == '__main__':
    unittest.main()
