import unittest
from model.user import User
from model.place import Place
from model.review import Review
from data_manager import DataManager

class TestReview(unittest.TestCase):

    def setUp(self):
        User._emails.clear()  # Limpia los emails registrados antes de cada prueba
        self.data_manager = DataManager("test_data")
        self.user = User("reviewer@example.com", "password", "Reviewer", "User")
        self.place = Place(
            name="Sample Place",
            description="A sample place",
            address="123 Sample St",
            city="Sample City",
            latitude=10.0,
            longitude=20.0,
            host=self.user,
            number_of_rooms=3,
            number_of_bathrooms=2,
            price_per_night=100.0,
            max_guests=4
        )

    def tearDown(self):
        import shutil
        shutil.rmtree("test_data")

    def test_create_review(self):
        review = Review(self.user, self.place, "Great place!", 5)
        self.data_manager.save(review)
        retrieved_review = self.data_manager.get(review.id, "review")
        self.assertIsNotNone(retrieved_review)
        self.assertEqual(retrieved_review["text"], "Great place!")

    def test_no_duplicate_reviews_on_same_day(self):
        review1 = Review(self.user, self.place, "Great place!", 5)
        self.data_manager.save(review1)
        review2 = Review(self.user, self.place, "Great place!", 5)
        with self.assertRaises(ValueError):
            self.data_manager.save(review2)

    def test_update_review(self):
        review = Review(self.user, self.place, "Great place!", 5)
        self.data_manager.save(review)
        review.text = "Updated review"
        self.data_manager.update(review)
        updated_review = self.data_manager.get(review.id, "review")
        self.assertEqual(updated_review["text"], "Updated review")

if __name__ == '__main__':
    unittest.main()
