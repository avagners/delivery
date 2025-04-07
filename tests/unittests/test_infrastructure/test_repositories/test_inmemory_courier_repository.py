import unittest

from core.domain.model.courier_aggregate.courier import Courier, CourierStatus, CourierStatusValue
from core.domain.model.shared_kernel.location import Location
from infrastructure.adapters.in_memory.courier_repository_in_memory import InMemoryCourierRepository


class TestCourierRepository(unittest.TestCase):
    """Тесты для репозитория курьеров"""

    def setUp(self):
        """Инициализация тестовых данных перед каждым тестом"""
        self.repo = InMemoryCourierRepository()
        self.location = Location(1, 2)
        self.courier1 = Courier("John", "bike", 2, self.location)
        self.courier2 = Courier("Mike", "car", 3, self.location)
        self.courier2.set_busy()

    def test_add_and_get_courier(self):
        """Проверка добавления курьера и его получения по ID"""
        self.repo.add(self.courier1)
        retrieved = self.repo.get_by_id(self.courier1.id)
        self.assertEqual(retrieved, self.courier1)

    def test_add_existing_courier_raises_error(self):
        """Проверка обработки попытки добавления дубликата курьера"""
        self.repo.add(self.courier1)
        with self.assertRaises(ValueError):
            self.repo.add(self.courier1)

    def test_update_courier(self):
        """Проверка обновления данных курьера в репозитории"""
        self.repo.add(self.courier1)
        self.courier1.set_busy()
        self.repo.update(self.courier1)
        updated = self.repo.get_by_id(self.courier1.id)
        self.assertEqual(updated.status, CourierStatus(CourierStatusValue.BUSY))

    def test_get_all_free(self):
        """Проверка получения всех свободных курьеров"""
        self.repo.add(self.courier1)
        self.repo.add(self.courier2)
        result = self.repo.get_all_free()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], self.courier1)


if __name__ == "__main__":
    unittest.main()
