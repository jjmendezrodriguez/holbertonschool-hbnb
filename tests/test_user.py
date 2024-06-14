import unittest
from model.user import User

class TestUser(unittest.TestCase):

    def setUp(self):
        User._emails.clear()  # Limpia los emails registrados antes de cada prueba

    def test_create_user(self):
        user = User("test@example.com", "password", "John", "Doe")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertIsNotNone(user.id)
        self.assertIsNotNone(user.created_at)
        self.assertIsNotNone(user.updated_at)

    def test_unique_email(self):
        user1 = User("unique@example.com", "password", "Jane", "Doe")
        with self.assertRaises(ValueError):
            User("unique@example.com", "password", "John", "Smith")

    def test_update_user(self):
        user = User("update@example.com", "password", "Update", "User")
        user.update(email="new@example.com", first_name="New")
        self.assertEqual(user.email, "new@example.com")
        self.assertEqual(user.first_name, "New")
        self.assertNotEqual(user.updated_at, user.created_at)

if __name__ == '__main__':
    unittest.main()
