import unittest
from models.place import Place

class TestPlace(unittest.TestCase):
    def test_place_creation(self):
        place = Place(name="Nice Place", description="A nice place to stay.", address="123 Main St", city_id="1", latitude=45.0, longitude=-75.0, host_id=None, number_of_rooms=2, number_of_bathrooms=1, price_per_night=100, max_guests=4)
        self.assertEqual(place.name, "Nice Place")
        self.assertEqual(place.description, "A nice place to stay.")
        self.assertEqual(place.address, "123 Main St")

    def test_set_host(self):
        place = Place(name="Nice Place", description="A nice place to stay.", address="123 Main St", city_id="1", latitude=45.0, longitude=-75.0, host_id=None, number_of_rooms=2, number_of_bathrooms=1, price_per_night=100, max_guests=4)
        place.set_host("host123")
        self.assertEqual(place.host_id, "host123")
        with self.assertRaises(ValueError):
            place.set_host("host456")

if __name__ == '__main__':
    unittest.main()