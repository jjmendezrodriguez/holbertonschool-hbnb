import unittest
from model.user import User
from model.place import Place
from model.city import City
from persistence.data_manager import DataManager

class TestPlace(unittest.TestCase):

    def setUp(self):
        User._emails.clear()  # Limpia los emails registrados antes de cada prueba
        self.data_manager = DataManager("test_data")
        self.host = User("host@example.com", "password", "Host", "User")
        self.city = City("Sample City", "SC")

    def tearDown(self):
        import shutil
        shutil.rmtree("test_data")

    def test_create_place(self):
        place = Place(
            name="Sample Place",
            description="A sample place",
            address="123 Sample St",
            city=self.city,
            latitude=10.0,
            longitude=20.0,
            host=self.host,
            number_of_rooms=3,
            number_of_bathrooms=2,
            price_per_night=100.0,
            max_guests=4
        )
        self.assertEqual(place.name, "Sample Place")
        self.assertEqual(place.city, self.city)
        self.assertEqual(place.host, self.host)
        self.assertIsNotNone(place.id)
        self.assertIsNotNone(place.created_at)
        self.assertIsNotNone(place.updated_at)

    def test_update_place(self):
        place = Place(
            name="Sample Place",
            description="A sample place",
            address="123 Sample St",
            city=self.city,
            latitude=10.0,
            longitude=20.0,
            host=self.host,
            number_of_rooms=3,
            number_of_bathrooms=2,
            price_per_night=100.0,
            max_guests=4
        )
        place.update(name="Updated Place", price_per_night=120.0)
        self.assertEqual(place.name, "Updated Place")
        self.assertEqual(place.price_per_night, 120.0)
        self.assertNotEqual(place.updated_at, place.created_at)

if __name__ == '__main__':
    unittest.main()
