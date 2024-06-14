import unittest
from models.user import User

class TestUser(unittest.TestCase):
    def test_user_creation(self):
        user = User(email="test@example.com", first_name="John", last_name="Doe")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")

    def test_duplicate_email(self):
        user1 = User(email="unique@example.com", first_name="Alice", last_name="Smith")
        with self.assertRaises(ValueError):
            user2 = User(email="unique@example.com", first_name="Bob", last_name="Brown")

if __name__ == '__main__':
    unittest.main()