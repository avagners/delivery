import unittest

from core.domain.model.order_aggregate.order_status import OrderStatus


class TestOrderStatus(unittest.TestCase):
    """Тесты для OrderStatus"""

    def test_valid_statuses(self):
        """Проверяем, что можно создать объект с допустимыми статусами"""
        created_status = OrderStatus.set_created()
        assigned_status = OrderStatus.set_assigned()
        completed_status = OrderStatus.set_completed()

        self.assertEqual(created_status.name.value, "created")
        self.assertEqual(assigned_status.name.value, "assigned")
        self.assertEqual(completed_status.name.value, "completed")

    def test_invalid_status(self):
        """Проверяем, что при создании с недопустимым статусом выбрасывается ValueError"""
        with self.assertRaises(ValueError):
            OrderStatus("invalid_status")

    def test_equality(self):
        """Проверяем, что объекты с одинаковым статусом равны, а с разными — нет"""
        status1 = OrderStatus.set_created()
        status2 = OrderStatus.set_created()
        status3 = OrderStatus.set_completed()

        self.assertEqual(status1, status2)
        self.assertNotEqual(status1, status3)

    def test_hash(self):
        """Проверяем, что hash одинаков для одинаковых статусов"""
        status1 = OrderStatus.set_assigned()
        status2 = OrderStatus.set_assigned()

        self.assertEqual(hash(status1), hash(status2))

    def test_string_representation(self):
        """Проверяем, что строковое представление соответствует значению"""
        status = OrderStatus.set_completed()
        self.assertEqual(str(status), "completed")


if __name__ == "__main__":
    unittest.main()
