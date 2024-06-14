import unittest
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models.country import Country
from models.city import City
from persistance.data_manager import DataManager

class TestDataManager(unittest.TestCase):
    def setUp(self):
        self.data_manager = DataManager()
        self.user = User(email="test@example.com", first_name="John", last_name="Doe")
        self.place = Place(name="Nice Place", description="A nice place to stay.", address="123 Main St", city_id="1", latitude=45.0, longitude=-75.0, host_id="1", number_of_rooms=2, number_of_bathrooms=1, price_per_night=100, max_guests=4)
        self.review = Review(user_id=self.user.id, place_id=self.place.id, rating=5, comment="Great place!")
        self.amenity = Amenity(name="WiFi")
        self.country = Country(code="US", name="United States")
        self.city = City(name="New York", country_code="US")

    def test_save_and_get_user(self):
        self.data_manager.save(self.user)
        retrieved_user = self.data_manager.get(self.user.id, 'User')
        self.assertEqual(self.user.email, retrieved_user.email)

    def test_update_user(self):
        self.data_manager.save(self.user)
        self.user.first_name = "Jane"
        self.data_manager.update(self.user)
        retrieved_user = self.data_manager.get(self.user.id, 'User')
        self.assertEqual(self.user.first_name, retrieved_user.first_name)

    def test_delete_user(self):
        self.data_manager.save(self.user)
        self.data_manager.delete(self.user.id, 'User')
        retrieved_user = self.data_manager.get(self.user.id, 'User')
        self.assertIsNone(retrieved_user)

    def test_save_and_get_place(self):
        self.data_manager.save(self.place)
        retrieved_place = self.data_manager.get(self.place.id, 'Place')
        self.assertEqual(self.place.name, retrieved_place.name)

    def test_save_and_get_review(self):
        self.data_manager.save(self.review)
        retrieved_review = self.data_manager.get(self.review.id, 'Review')
        self.assertEqual(self.review.comment, retrieved_review.comment)

    def test_save_and_get_amenity(self):
        self.data_manager.save(self.amenity)
        retrieved_amenity = self.data_manager.get(self.amenity.id, 'Amenity')
        self.assertEqual(self.amenity.name, retrieved_amenity.name)

    def test_save_and_get_country(self):
        self.data_manager.save(self.country)
        retrieved_country = self.data_manager.get(self.country.code, 'Country')
        self.assertEqual(self.country.name, retrieved_country.name)

    def test_save_and_get_city(self):
        self.data_manager.save(self.city)
        retrieved_city = self.data_manager.get(self.city.id, 'City')
        self.assertEqual(self.city.name, retrieved_city.name)

if __name__ == '__main__':
    unittest.main()