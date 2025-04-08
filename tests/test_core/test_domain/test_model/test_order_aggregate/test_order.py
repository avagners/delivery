import unittest
import uuid

from core.domain.model.shared_kernel.location import Location
from core.domain.model.order_aggregate.order import Order
from core.domain.model.order_aggregate.order_status import OrderStatusValue
from core.domain.model.shared_kernel.business_rule_exception import BusinessRuleBrokenException


class TestOrder(unittest.TestCase):
    """Тесты для Order"""

    def setUp(self):
        """Настройка перед каждым тестом"""
        self.valid_order_id = uuid.uuid4()
        self.valid_location = Location(5, 5)

    def test_create_order_success(self):
        """Тест успешного создания заказа"""
        order = Order(self.valid_order_id, self.valid_location)

        self.assertEqual(order.id, self.valid_order_id)
        self.assertEqual(order.location, self.valid_location)
        self.assertEqual(order.status.name, OrderStatusValue.CREATED)
        self.assertIsNone(order.courier_id)

    def test_create_order_invalid_id(self):
        """Тест ошибки при создании заказа с некорректным ID"""
        with self.assertRaises(BusinessRuleBrokenException) as context:
            Order(uuid.UUID(int=0), self.valid_location)

        self.assertEqual(str(context.exception.rule), "Order ID cannot be empty or zero.")

    def test_create_order_invalid_location(self):
        """Тест ошибки при создании заказа без локации"""
        with self.assertRaises(BusinessRuleBrokenException) as context:
            Order(self.valid_order_id, None)

        self.assertEqual(str(context.exception.rule), "Order location cannot be empty.")

    def test_assign_to_courier_success(self):
        """Тест успешного назначения курьера"""
        order = Order(self.valid_order_id, self.valid_location)
        courier_id = uuid.uuid4()

        order.assign_to_courier(courier_id)

        self.assertEqual(order.status.name, OrderStatusValue.ASSIGNED)
        self.assertEqual(order.courier_id, courier_id)

    def test_assign_to_courier_invalid_status(self):
        """Тест ошибки при назначении курьера, если заказ уже назначен"""
        order = Order(self.valid_order_id, self.valid_location)
        order.assign_to_courier(uuid.uuid4())

        with self.assertRaises(BusinessRuleBrokenException) as context:
            order.assign_to_courier(uuid.uuid4())

        self.assertEqual(str(context.exception.rule), "Order can only be assigned if it is in 'CREATED' status.")

    def test_complete_order_success(self):
        """Тест успешного завершения заказа"""
        order = Order(self.valid_order_id, self.valid_location)
        order.assign_to_courier(uuid.uuid4())

        order.complete()

        self.assertEqual(order.status.name, OrderStatusValue.COMPLETED)

    def test_complete_order_invalid_status(self):
        """Тест ошибки при завершении заказа, если он не был назначен"""
        order = Order(self.valid_order_id, self.valid_location)

        with self.assertRaises(BusinessRuleBrokenException) as context:
            order.complete()

        self.assertEqual(str(context.exception.rule), "Order can only be completed if it is in 'ASSIGNED' status.")


if __name__ == "__main__":
    unittest.main()
