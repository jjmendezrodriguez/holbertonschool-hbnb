import unittest  # Importa el módulo unittest para realizar pruebas unitarias.
from Model.place import Place  # Importa la clase Place del módulo model.place.
from Model.user import User  # Importa la clase User del módulo model.user.
from Model.city import City  # Importa la clase City del módulo model.city.

class TestPlace(unittest.TestCase):  # Define la clase de pruebas para Place.

    def setUp(self):
        # Inicializa datos comunes para las pruebas
        self.host = User("host@example.com", "password", "Host", "User")  # Crea un usuario anfitrión.
        self.city = City("Sample City", "Sample Country")  # Crea una ciudad.

    def test_create_place(self):
        # Prueba la creación de un lugar
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
        )  # Crea un objeto Place con los datos proporcionados.
        self.assertEqual(place.name, "Sample Place")  # Verifica que el nombre sea el esperado.
        self.assertEqual(place.city, self.city)  # Verifica que la ciudad sea la esperada.
        self.assertEqual(place.host, self.host)  # Verifica que el anfitrión sea el esperado.
        self.assertIsNotNone(place.id)  # Verifica que el id no sea None.
        self.assertIsNotNone(place.created_at)  # Verifica que la fecha de creación no sea None.
        self.assertIsNotNone(place.updated_at)  # Verifica que la fecha de actualización no sea None.

    def test_update_place(self):
        # Prueba la actualización de un lugar
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
        )  # Crea un objeto Place con los datos proporcionados.
        place.update(name="Updated Place", price_per_night=120.0)  # Actualiza el nombre y el precio por noche del lugar.
        self.assertEqual(place.name, "Updated Place")  # Verifica que el nombre sea el esperado.
        self.assertEqual(place.price_per_night, 120.0)  # Verifica que el precio por noche sea el esperado.
        self.assertNotEqual(place.updated_at, place.created_at)  # Verifica que la fecha de actualización sea diferente a la fecha de creación.

if __name__ == '__main__':
    unittest.main()  # Ejecuta las pruebas.
