import unittest
from uuid import UUID

from core.domain.model.shared_kernel.entity import BusinessRuleBrokenException
from core.domain.model.shared_kernel.location import Location
from core.domain.model.courier_aggregate.transport import Transport


class TestTransport(unittest.TestCase):
    def test_create_transport_with_valid_data(self):
        """Тест создания транспорта с валидными данными"""
        transport = Transport(name="Bike", speed=2)
        self.assertEqual(transport.name, "Bike")
        self.assertEqual(transport.speed, 2)
        self.assertIsInstance(transport.id, UUID)

    def test_create_transport_with_empty_name(self):
        """Тест создания транспорта с пустым названием"""
        with self.assertRaises(BusinessRuleBrokenException) as context:
            Transport(name="", speed=2)
        self.assertEqual(str(context.exception), "Business rule NotEmptyNameRule is broken: Name cannot be empty")

    def test_create_transport_with_invalid_speed(self):
        """Тест создания транспорта с невалидной скоростью"""
        with self.assertRaises(BusinessRuleBrokenException) as context:
            Transport(name="Bike", speed=0)
        self.assertEqual(str(context.exception), "Business rule ValidSpeedRule is broken: Speed must be between 1 and 3, but got 0")

        with self.assertRaises(BusinessRuleBrokenException) as context:
            Transport(name="Bike", speed=4)
        self.assertEqual(str(context.exception), "Business rule ValidSpeedRule is broken: Speed must be between 1 and 3, but got 4")

    def test_move_towards_same_location(self):
        """Тест перемещения, когда текущее и целевое местоположение совпадают"""
        transport = Transport(name="Bike", speed=2)
        current_location = Location(1, 1)
        target_location = Location(1, 1)

        new_location = transport.move_towards(current_location, target_location)
        self.assertEqual(new_location, current_location)

    def test_move_towards_horizontally(self):
        """Тест перемещения по горизонтали"""
        transport = Transport(name="Bike", speed=2)
        current_location = Location(1, 1)
        target_location = Location(5, 1)

        new_location = transport.move_towards(current_location, target_location)
        self.assertEqual(new_location, Location(3, 1))  # Перемещение на 2 клетки вправо

    def test_move_towards_vertically(self):
        """Тест перемещения по вертикали"""
        transport = Transport(name="Bike", speed=2)
        current_location = Location(1, 1)
        target_location = Location(1, 5)

        new_location = transport.move_towards(current_location, target_location)
        self.assertEqual(new_location, Location(1, 3))  # Перемещение на 2 клетки вниз

    def test_move_towards_negative_direction(self):
        """Тест перемещения в отрицательном направлении"""
        transport = Transport(name="Bike", speed=2)
        current_location = Location(5, 5)
        target_location = Location(3, 3)

        new_location = transport.move_towards(current_location, target_location)
        # Ожидаемый результат: 2 шага влево (по горизонтали)
        self.assertEqual(new_location, Location(3, 5))


if __name__ == "__main__":
    unittest.main()
