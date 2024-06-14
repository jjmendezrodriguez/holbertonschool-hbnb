import unittest
from model.user import User
from persistence.data_manager import DataManager

class TestDataManager(unittest.TestCase):

    def setUp(self):
        User._emails.clear()  # Limpia los emails registrados antes de cada prueba
        self.data_manager = DataManager("test_data")
        self.user = User("test@example.com", "password", "John", "Doe")

    def tearDown(self):
        import shutil
        shutil.rmtree("test_data")

    def test_save_and_get_user(self):
        self.data_manager.save(self.user)
        retrieved_user = self.data_manager.get(self.user.id, "user")
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user["email"], "test@example.com")

    def test_update_user(self):
        self.data_manager.save(self.user)
        self.user.first_name = "Jane"
        self.data_manager.update(self.user)
        updated_user = self.data_manager.get(self.user.id, "user")
        self.assertEqual(updated_user["first_name"], "Jane")

    def test_delete_user(self):
        self.data_manager.save(self.user)
        self.data_manager.delete(self.user.id, "user")
        deleted_user = self.data_manager.get(self.user.id, "user")
        self.assertIsNone(deleted_user)

if __name__ == '__main__':
    unittest.main()
