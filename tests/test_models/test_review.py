import unittest
from models.review import Review

class TestReview(unittest.TestCase):
    def test_review_creation(self):
        review = Review(user_id="user123", place_id="place123", rating=5, comment="Great place!")
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, "Great place!")

    def test_invalid_rating(self):
        with self.assertRaises(ValueError):
            review = Review(user_id="user123", place_id="place123", rating=6, comment="Excellent!")

if __name__ == '__main__':
    unittest.main()