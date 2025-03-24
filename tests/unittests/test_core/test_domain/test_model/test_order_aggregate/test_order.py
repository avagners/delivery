import unittest
import uuid

from core.domain.model.shared_kernel.location import Location
from core.domain.model.order_aggregate.order import Order
from core.domain.model.order_aggregate.order_status import OrderStatus, OrderStatusValue


class TestOrder(unittest.TestCase):
    """Тесты для бизнес-логики Order"""

    def setUp(self):
        """Подготовка данных перед каждым тестом"""
        self.order_id = uuid.uuid4()
        self.location = Location(5, 5)  # Валидная локация
        self.order = Order(self.order_id, self.location)

    def test_order_creation(self):
        """Тест создания заказа"""
        self.assertEqual(self.order.id, self.order_id)
        self.assertEqual(self.order.location, self.location)
        self.assertEqual(self.order.status, OrderStatus(OrderStatusValue.CREATED))
        self.assertIsNone(self.order.courier_id)

    def test_order_creation_with_invalid_id(self):
        """Тест создания заказа с пустым ID"""
        with self.assertRaises(ValueError) as ctx:
            Order(None, self.location)
        self.assertEqual(str(ctx.exception), "Order ID is required")

    def test_order_creation_with_invalid_location(self):
        """Тест создания заказа без Location"""
        with self.assertRaises(ValueError) as ctx:
            Order(self.order_id, None)
        self.assertEqual(str(ctx.exception), "Location is required")

    def test_assign_order_to_courier(self):
        """Тест назначения курьера"""
        courier_id = uuid.uuid4()
        self.order.assign_to_courier(courier_id)

        self.assertEqual(self.order.status, OrderStatus(OrderStatusValue.ASSIGNED))
        self.assertEqual(self.order.courier_id, courier_id)

    def test_assign_order_already_assigned(self):
        """Тест попытки повторного назначения"""
        courier_id_1 = uuid.uuid4()
        courier_id_2 = uuid.uuid4()

        self.order.assign_to_courier(courier_id_1)

        with self.assertRaises(ValueError) as ctx:
            self.order.assign_to_courier(courier_id_2)

        self.assertEqual(str(ctx.exception), "Cannot assign an already assigned or completed order.")
        self.assertEqual(self.order.courier_id, courier_id_1)  # Курьер не должен измениться

    def test_assign_order_when_completed(self):
        """Тест назначения заказа после завершения"""
        courier_id = uuid.uuid4()
        self.order.assign_to_courier(courier_id)
        self.order.complete()

        with self.assertRaises(ValueError) as ctx:
            self.order.assign_to_courier(uuid.uuid4())

        self.assertEqual(str(ctx.exception), "Cannot assign an already assigned or completed order.")

    def test_complete_order(self):
        """Тест успешного завершения заказа"""
        courier_id = uuid.uuid4()
        self.order.assign_to_courier(courier_id)
        self.order.complete()

        self.assertEqual(self.order.status, OrderStatus(OrderStatusValue.COMPLETED))

    def test_complete_unassigned_order(self):
        """Тест завершения заказа, который не был назначен"""
        with self.assertRaises(ValueError) as ctx:
            self.order.complete()
        self.assertEqual(str(ctx.exception), "Cannot complete an order that has not been assigned.")

    def test_assign_order_with_invalid_courier_id(self):
        """Тест назначения заказа с пустым ID курьера"""
        with self.assertRaises(ValueError) as ctx:
            self.order.assign_to_courier(None)
        self.assertEqual(str(ctx.exception), "Courier ID is required")


if __name__ == "__main__":
    unittest.main()
