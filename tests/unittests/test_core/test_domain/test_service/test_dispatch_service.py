import unittest
from uuid import uuid4

from core.domain.model.courier_aggregate.courier import Courier
from core.domain.model.order_aggregate.order import Order
from core.domain.services.dispatch_service import DispatchService
from core.domain.model.shared_kernel.location import Location
from core.domain.model.courier_aggregate.courier import CourierStatusValue
from core.domain.model.courier_aggregate.courier import CourierStatus


class TestDispatchService(unittest.TestCase):

    def setUp(self):
        """Настраиваем тестовые данные"""
        self.order_location = Location(5, 5)
        self.order = Order(uuid4(), self.order_location)

        # Создаем курьеров с разными локациями
        self.courier1 = Courier("Иван", "Пешком", 1, Location(1, 1))
        self.courier2 = Courier("Петя", "Велосипед", 2, Location(1, 1))
        self.courier3 = Courier("Вася", "Машина", 3, Location(1, 1))
        self.couriers = [self.courier2, self.courier1, self.courier3]

    def test_dispatch_returns_closest_free_courier(self):
        """Тест, что возвращается самый лучший курьер"""
        result = DispatchService.dispatch(self.order, self.couriers)

        self.assertEqual(result, self.courier3)

    def test_dispatch_raises_error_when_no_free_couriers(self):
        """Тест, что выбрасывается исключение, когда нет свободных курьеров"""
        busy_couriers = []
        for c in self.couriers:
            c.status = CourierStatus(CourierStatusValue.BUSY)
            busy_couriers.append(c)

        with self.assertRaises(ValueError) as context:
            DispatchService.dispatch(self.order, busy_couriers)

        self.assertEqual(str(context.exception), "No available couriers")

    def test_dispatch_works_with_single_free_courier(self):
        """Тест, что сервис работает, когда есть только один свободный курьер"""
        couriers = [self.courier2]
        result = DispatchService.dispatch(self.order, couriers)
        self.assertEqual(result, self.courier2)

    def test_dispatch_ignores_busy_couriers(self):
        """Тест, что занятые курьеры игнорируются"""
        self.courier2.status = CourierStatus(CourierStatusValue.BUSY)
        couriers = [self.courier2, self.courier1]

        result = DispatchService.dispatch(self.order, couriers)

        self.assertEqual(result, self.courier1)

    def test_dispatch_with_empty_couriers_list_raises_error(self):
        """Тест, что пустой список курьеров вызывает исключение"""
        with self.assertRaises(ValueError) as context:
            DispatchService.dispatch(self.order, [])

        self.assertEqual(str(context.exception), "No available couriers")


if __name__ == '__main__':
    unittest.main()
