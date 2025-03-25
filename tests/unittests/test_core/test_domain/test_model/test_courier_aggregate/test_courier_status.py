import unittest

from core.domain.model.courier_aggregate.courier_status import CourierStatus, CourierStatusValue


class TestCourierStatus(unittest.TestCase):
    """Тесты для CourierStatus"""

    def test_valid_statuses(self):
        """Проверяем, что можно создать объект с допустимыми статусами"""
        free_status = CourierStatus(CourierStatusValue.FREE)
        busy_status = CourierStatus(CourierStatusValue.BUSY)

        self.assertEqual(free_status.name, CourierStatusValue.FREE)
        self.assertEqual(busy_status.name, CourierStatusValue.BUSY)

    def test_invalid_status(self):
        """Проверяем, что при создании с недопустимым статусом выбрасывается ValueError"""
        with self.assertRaises(ValueError):
            CourierStatus("invalid_status")

    def test_equality(self):
        """Проверяем, что объекты с одинаковым статусом равны, а с разными — нет"""
        status1 = CourierStatus(CourierStatusValue.FREE)
        status2 = CourierStatus(CourierStatusValue.FREE)
        status3 = CourierStatus(CourierStatusValue.BUSY)

        self.assertEqual(status1, status2)
        self.assertNotEqual(status1, status3)

    def test_hash(self):
        """Проверяем, что hash одинаков для одинаковых статусов"""
        status1 = CourierStatus(CourierStatusValue.FREE)
        status2 = CourierStatus(CourierStatusValue.FREE)

        self.assertEqual(hash(status1), hash(status2))

    def test_string_representation(self):
        """Проверяем, что строковое представление соответствует значению"""
        status = CourierStatus(CourierStatusValue.FREE)
        self.assertEqual(str(status), "free")


if __name__ == "__main__":
    unittest.main()
