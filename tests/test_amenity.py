import unittest  # Importa el módulo unittest para realizar pruebas unitarias.
from Model.amenity import Amenity  # Importa la clase Amenity del módulo model.amenity.
import os
import json

class TestAmenity(unittest.TestCase):  # Define la clase de pruebas para Amenity.

    def setUp(self):
        # Se ejecuta antes de cada prueba. Asegura que no haya un archivo JSON residual de pruebas anteriores.
        self.filepath = 'data/amenities.json'
        if os.path.exists(self.filepath):
            os.remove(self.filepath)

    def test_create_amenity(self):
        # Prueba la creación de una comodidad
        amenity = Amenity(name="WiFi", description="High-speed wireless internet")
        self.assertEqual(amenity.name, "WiFi")  # Verifica que el nombre sea el esperado.
        self.assertEqual(amenity.description, "High-speed wireless internet")  # Verifica que la descripción sea la esperada.
        self.assertIsNotNone(amenity.id)  # Verifica que el id no sea None.
        self.assertIsNotNone(amenity.created_at)  # Verifica que la fecha de creación no sea None.
        self.assertIsNotNone(amenity.updated_at)  # Verifica que la fecha de actualización no sea None.

    def test_update_amenity(self):
        # Prueba la actualización de una comodidad
        amenity = Amenity(name="WiFi", description="High-speed wireless internet")
        amenity.update(name="Free WiFi", description="Complimentary high-speed wireless internet")
        self.assertEqual(amenity.name, "Free WiFi")  # Verifica que el nombre sea el esperado.
        self.assertEqual(amenity.description, "Complimentary high-speed wireless internet")  # Verifica que la descripción sea la esperada.
        self.assertNotEqual(amenity.updated_at, amenity.created_at)  # Verifica que la fecha de actualización sea diferente a la fecha de creación.

    def test_no_duplicate_amenities(self):
        # Prueba que no se puedan crear comodidades duplicadas
        amenity1 = Amenity(name="WiFi", description="High-speed wireless internet")
        amenity1.save_to_json()
        with self.assertRaises(ValueError):  # Verifica que se lance un error al intentar crear una comodidad duplicada.
            amenity2 = Amenity(name="WiFi", description="High-speed wireless internet")
            amenity2.save_to_json()

    def tearDown(self):
        # Se ejecuta después de cada prueba. Limpia el archivo JSON si fue creado.
        if os.path.exists(self.filepath):
            os.remove(self.filepath)

if __name__ == '__main__':
    unittest.main()  # Ejecuta las pruebas.
