import unittest  # Importa el módulo unittest para realizar pruebas unitarias.
import uuid  # Importa el módulo uuid para manejar identificadores únicos.
from datetime import datetime  # Importa datetime del módulo datetime para manejar fechas y horas.
from Model.user import User  # Importa la clase User del módulo model.user.
from Persistence.data_manager import DataManager  # Importa la clase DataManager del módulo persistence.data_manager.

class TestDataManager(unittest.TestCase):  # Define la clase de pruebas para DataManager.

    def setUp(self):  # Método que se ejecuta antes de cada prueba.
        self.data_manager = DataManager("test_data")  # Crea una instancia de DataManager con un directorio de prueba.
        self.user = User("test@example.com", "password", "John", "Doe")  # Crea un objeto User.

    def tearDown(self):  # Método que se ejecuta después de cada prueba.
        import shutil  # Importa el módulo shutil para operaciones con el sistema de archivos.
        shutil.rmtree("test_data")  # Elimina el directorio de prueba.

    def test_save_and_get_user(self):  # Prueba para verificar guardar y obtener un usuario.
        self.data_manager.save(self.user)  # Guarda el usuario.
        retrieved_user = self.data_manager.get(self.user.id, "user")  # Obtiene el usuario.
        self.assertIsNotNone(retrieved_user)  # Verifica que el usuario no sea None.
        self.assertEqual(retrieved_user["email"], "test@example.com")  # Verifica que el email del usuario sea el esperado.

    def test_update_user(self):  # Prueba para verificar la actualización de un usuario.
        self.data_manager.save(self.user)  # Guarda el usuario.
        self.user.first_name = "Jane"  # Actualiza el primer nombre del usuario.
        self.data_manager.update(self.user)  # Actualiza el usuario en el almacenamiento.
        updated_user = self.data_manager.get(self.user.id, "user")  # Obtiene el usuario actualizado.
        self.assertEqual(updated_user["first_name"], "Jane")  # Verifica que el primer nombre sea el esperado.

    def test_delete_user(self):  # Prueba para verificar la eliminación de un usuario.
        self.data_manager.save(self.user)  # Guarda el usuario.
        self.data_manager.delete(self.user.id, "user")  # Elimina el usuario.
        deleted_user = self.data_manager.get(self.user.id, "user")  # Intenta obtener el usuario eliminado.
        self.assertIsNone(deleted_user)  # Verifica que el usuario sea None.

if __name__ == '__main__':
    unittest.main()  # Ejecuta las pruebas.
