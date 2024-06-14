import unittest  # Importa el módulo unittest para realizar pruebas unitarias.
from Model.user import User  # Importa la clase User del módulo model.user.

class TestUser(unittest.TestCase):  # Define la clase de pruebas para User.

    def setUp(self):
        # Se ejecuta antes de cada prueba. Inicializa un conjunto vacío de emails para cada prueba.
        User._emails = {}

    def test_create_user(self):
        user = User("test@example.com", "password", "John", "Doe")  # Crea un objeto User.
        self.assertEqual(user.email, "test@example.com")  # Verifica que el email sea el esperado.
        self.assertEqual(user.first_name, "John")  # Verifica que el primer nombre sea el esperado.
        self.assertEqual(user.last_name, "Doe")  # Verifica que el apellido sea el esperado.
        self.assertIsNotNone(user.id)  # Verifica que el id no sea None.
        self.assertIsNotNone(user.created_at)  # Verifica que la fecha de creación no sea None.
        self.assertIsNotNone(user.updated_at)  # Verifica que la fecha de actualización no sea None.

    def test_unique_email(self):
        user1 = User("unique@example.com", "password", "Jane", "Doe")  # Crea un usuario con un email único.
        with self.assertRaises(ValueError):  # Verifica que se lance un error al intentar crear un usuario con el mismo email.
            User("unique@example.com", "password", "John", "Smith")

    def test_update_user(self):
        user = User("update@example.com", "password", "Update", "User")  # Crea un usuario.
        user.update(email="new@example.com", first_name="New")  # Actualiza el email y el primer nombre del usuario.
        self.assertEqual(user.email, "new@example.com")  # Verifica que el email sea el esperado.
        self.assertEqual(user.first_name, "New")  # Verifica que el primer nombre sea el esperado.
        self.assertNotEqual(user.updated_at, user.created_at)  # Verifica que la fecha de actualización sea diferente a la fecha de creación.

if __name__ == '__main__':
    unittest.main()  # Ejecuta las pruebas.
