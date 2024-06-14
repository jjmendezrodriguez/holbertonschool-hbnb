import unittest  # Importa el módulo unittest para realizar pruebas unitarias.
from Model.country import Country  # Importa la clase Country del módulo model.country.
from Model.city import City  # Importa la clase City del módulo model.city.

class TestCountry(unittest.TestCase):  # Define la clase de pruebas para Country.

    def setUp(self):
        # Se ejecuta antes de cada prueba. Inicializa una lista vacía de ciudades para cada prueba.
        self.country = Country(name="Sample Country", code="SC")

    def test_create_country(self):
        # Prueba la creación de un país
        self.assertEqual(self.country.name, "Sample Country")  # Verifica que el nombre sea el esperado.
        self.assertEqual(self.country.code, "SC")  # Verifica que el código sea el esperado.
        self.assertIsNotNone(self.country.id)  # Verifica que el id no sea None.
        self.assertIsNotNone(self.country.created_at)  # Verifica que la fecha de creación no sea None.
        self.assertIsNotNone(self.country.updated_at)  # Verifica que la fecha de actualización no sea None.

    def test_update_country(self):
        # Prueba la actualización de un país
        self.country.update(name="Updated Country", code="UC")  # Actualiza el nombre y el código del país.
        self.assertEqual(self.country.name, "Updated Country")  # Verifica que el nombre sea el esperado.
        self.assertEqual(self.country.code, "UC")  # Verifica que el código sea el esperado.
        self.assertNotEqual(self.country.updated_at, self.country.created_at)  # Verifica que la fecha de actualización sea diferente a la fecha de creación.

    def test_add_city_to_country(self):
        # Prueba la adición de una ciudad a un país
        city = City(name="Sample City", country=self.country)
        self.country.cities.append(city)  # Añade una ciudad al país.
        self.assertIn(city, self.country.cities)  # Verifica que la ciudad esté en la lista de ciudades del país.

if __name__ == '__main__':
    unittest.main()  # Ejecuta las pruebas.
