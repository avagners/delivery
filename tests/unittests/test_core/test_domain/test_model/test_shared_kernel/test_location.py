import unittest

from core.domain.model.shared_kernel.location import Location, LocationSize


class TestLocation(unittest.TestCase):
    def test_valid_location(self):
        location = Location(LocationSize.MIN.value, LocationSize.MIN.value)
        self.assertEqual(location.x, LocationSize.MIN.value)
        self.assertEqual(location.y, LocationSize.MIN.value)

    def test_invalid_location(self):
        with self.assertRaises(ValueError):
            Location(LocationSize.MIN.value - 1, LocationSize.MIN.value)
        with self.assertRaises(ValueError):
            Location(LocationSize.MAX.value + 1, LocationSize.MAX.value)

    def test_equality(self):
        location1 = Location(LocationSize.MIN.value, LocationSize.MIN.value)
        location2 = Location(LocationSize.MIN.value, LocationSize.MIN.value)
        location3 = Location(LocationSize.MAX.value, LocationSize.MAX.value)
        self.assertEqual(location1, location2)
        self.assertNotEqual(location1, location3)

    def test_distance(self):
        location1 = Location(LocationSize.MIN.value, LocationSize.MIN.value)
        location2 = Location(3, 4)
        self.assertEqual(location1.distance_to(location2), 5)

    def test_create_random_location(self):
        location = Location.create_random_location()
        self.assertTrue(
            LocationSize.MIN.value <= location.x <= LocationSize.MAX.value
        )
        self.assertTrue(
            LocationSize.MIN.value <= location.y <= LocationSize.MAX.value
        )

    def test_immutability(self):
        location = Location(LocationSize.MIN.value, LocationSize.MIN.value)
        with self.assertRaises(AttributeError):
            location.x = 2  # Попытка изменить атрибут


if __name__ == '__main__':
    unittest.main()
