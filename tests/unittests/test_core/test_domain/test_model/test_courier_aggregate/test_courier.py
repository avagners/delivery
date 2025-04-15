import unittest

from core.domain.model.shared_kernel.location import Location
from core.domain.model.shared_kernel.entity import BusinessRuleBrokenException
from core.domain.model.courier_aggregate.courier import Courier
from core.domain.model.courier_aggregate.courier_status import CourierStatus, CourierStatusValue


class TestCourier(unittest.TestCase):
    def setUp(self):
        """Настраиваем тестовые данные"""
        self.location = Location(1, 1)
        self.courier = Courier("Иван", "Велосипед", 2, self.location)

    def test_courier_creation(self):
        """Тест создания курьера"""
        self.assertEqual(self.courier.name, "Иван")
        self.assertEqual(self.courier.transport.name, "Велосипед")
        self.assertEqual(self.courier.transport.speed, 2)
        self.assertEqual(self.courier.location, self.location)
        self.assertEqual(self.courier.status, CourierStatus(CourierStatusValue.FREE))

    def test_invalid_courier_creation(self):
        """Тест ошибок при создании курьера"""
        with self.assertRaises(BusinessRuleBrokenException):
            Courier("", "Велосипед", 2, self.location)  # Пустое имя

        with self.assertRaises(BusinessRuleBrokenException):
            Courier("Иван", "", 2, self.location)  # Пустое название транспорта

        with self.assertRaises(BusinessRuleBrokenException):
            Courier("Иван", "Велосипед", 0, self.location)  # Нулевая скорость транспорта

        with self.assertRaises(BusinessRuleBrokenException):
            Courier("Иван", "Велосипед", -1, self.location)  # Отрицательная скорость транспорта

        with self.assertRaises(BusinessRuleBrokenException):
            Courier("Иван", "Велосипед", 4, self.location)  # Cкорость транспорта больше 3

        with self.assertRaises(BusinessRuleBrokenException):
            Courier("Иван", "Велосипед", 2, None)  # Отсутствует локация

    def test_set_status_busy(self):
        """Тест установки статуса 'занят'"""
        self.courier.set_busy()
        self.assertEqual(self.courier.status, CourierStatus(CourierStatusValue.BUSY))

    def test_set_status_free(self):
        """Тест установки статуса 'свободен'"""
        self.courier.set_busy()
        self.courier.set_free()
        self.assertEqual(self.courier.status, CourierStatus(CourierStatusValue.FREE))

    def test_calc_steps_to_location(self):
        """Тест расчета шагов до заказа"""
        target_location = Location(5, 5)
        steps = self.courier.calc_steps_to_location(target_location)
        self.assertEqual(steps, 4)  # Дистанция 8, скорость 2 → 4 шага

    def test_move_towards(self):
        """Тест перемещения курьера на 1 шаг"""
        target_location = Location(5, 5)
        old_location = self.courier.location
        self.courier.move_towards(target_location)
        self.assertNotEqual(self.courier.location, old_location)  # Курьер должен сдвинуться

    def test_invalid_calc_steps_to_location(self):
        """Тест ошибки, если передать не Location"""
        with self.assertRaises(ValueError):
            self.courier.calc_steps_to_location("неверный тип")

    def test_invalid_move_towards(self):
        """Тест ошибки, если передать не Location"""
        with self.assertRaises(ValueError):
            self.courier.move_towards("неверный тип")


if __name__ == "__main__":
    unittest.main()
