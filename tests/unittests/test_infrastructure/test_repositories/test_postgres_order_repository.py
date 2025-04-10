import unittest
import uuid
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from core.domain.model.order_aggregate.order import Order
from core.domain.model.order_aggregate.order_status import OrderStatusValue
from core.domain.model.shared_kernel.location import Location

from infrastructure.adapters.postgres.order_repository import OrderRepositoryImpl
from infrastructure.adapters.postgres.models import OrderModel


class TestOrderRepository(unittest.TestCase):
    def setUp(self):
        self.mock_session = MagicMock(spec=Session)
        self.repo = OrderRepositoryImpl(self.mock_session)
        self.sample_order_id = uuid.uuid4()
        self.sample_order = Order(
            order_id=self.sample_order_id,
            location=Location(5, 5)
        )
        self.courier_id = uuid.uuid4()

    def test_add_order(self):
        # Настраиваем mock для get_by_id (возвращаем None - заказ не существует)
        self.mock_session.get.return_value = None

        self.repo.add(self.sample_order)

        self.mock_session.add.assert_called_once()
        args, _ = self.mock_session.add.call_args
        order_model = args[0]

        self.assertIsInstance(order_model, OrderModel)
        self.assertEqual(order_model.id, self.sample_order_id)
        self.assertEqual(order_model.location_x, 5)
        self.assertEqual(order_model.status.value, "created")  # Проверяем raw value

    def test_get_one_created(self):
        mock_model = OrderModel(
            id=self.sample_order.id,
            location_x=5,
            location_y=5,
            status="created",
            courier_id=None
        )

        self.mock_session.query.return_value.filter.return_value.first.return_value = mock_model

        result = self.repo.get_one_created()

        self.assertIsNotNone(result)
        self.assertEqual(result.id, self.sample_order.id)
        self.assertEqual(result.status.name.value, "created")

    def test_assign_order(self):
        mock_model = OrderModel(
            id=self.sample_order.id,
            location_x=5,
            location_y=5,
            status="created",
            courier_id=None
        )

        self.mock_session.query.return_value.get.return_value = mock_model

        # Создаем заказ и назначаем курьера
        order = Order(
            order_id=self.sample_order.id,
            location=Location(5, 5)
        )
        order.assign_to_courier(self.courier_id)
        self.repo.update(order)
        self.assertEqual(mock_model.status, OrderStatusValue.ASSIGNED)
        self.assertEqual(mock_model.courier_id, self.courier_id)

    def test_get_all_assigned(self):
        mock_model = OrderModel(
            id=self.sample_order.id,
            location_x=5,
            location_y=5,
            status="assigned",
            courier_id=self.courier_id
        )

        self.mock_session.query.return_value.filter.return_value.all.return_value = [mock_model]

        result = list(self.repo.get_all_assigned())

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].status.name.value, "assigned")
        self.assertEqual(result[0].courier_id, self.courier_id)


if __name__ == '__main__':
    unittest.main()
