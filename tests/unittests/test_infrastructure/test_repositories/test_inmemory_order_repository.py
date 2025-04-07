import unittest
import uuid

from core.domain.model.order_aggregate.order import Order, OrderStatus, OrderStatusValue
from core.domain.model.shared_kernel.location import Location
from infrastructure.adapters.in_memory.order_repository_in_memory import InMemoryOrderRepository


class TestInMemoryOrderRepository(unittest.TestCase):
    """Тесты для репозитория заказов"""

    def setUp(self):
        """Инициализация тестовых данных перед каждым тестом"""
        self.repo = InMemoryOrderRepository()
        self.location = Location(1, 2)
        self.order1 = Order(uuid.uuid4(), self.location)
        self.order2 = Order(uuid.uuid4(), self.location)
        self.order2.assign_to_courier(uuid.uuid4())

    def test_add_and_get_order(self):
        """Проверка добавления заказа и его последующего получения по ID"""
        self.repo.add(self.order1)
        retrieved = self.repo.get_by_id(self.order1.id)
        self.assertEqual(retrieved, self.order1)

    def test_add_existing_order_raises_error(self):
        """Проверка обработки попытки добавления дубликата заказа"""
        self.repo.add(self.order1)
        with self.assertRaises(ValueError):
            self.repo.add(self.order1)

    def test_update_order(self):
        """Проверка обновления данных заказа в репозитории"""
        self.repo.add(self.order1)
        self.order1.assign_to_courier(uuid.uuid4())
        self.repo.update(self.order1)
        updated = self.repo.get_by_id(self.order1.id)
        self.assertEqual(updated.status, OrderStatus(OrderStatusValue.ASSIGNED))

    def test_get_one_created(self):
        """Проверка получения одного заказа со статусом Created"""
        self.repo.add(self.order1)
        self.repo.add(self.order2)
        result = self.repo.get_one_created()
        self.assertEqual(result, self.order1)

    def test_get_all_assigned(self):
        """Проверка получения всех заказов со статусом Assigned"""
        self.repo.add(self.order1)
        self.repo.add(self.order2)
        result = self.repo.get_all_assigned()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], self.order2)


if __name__ == "__main__":
    unittest.main()
