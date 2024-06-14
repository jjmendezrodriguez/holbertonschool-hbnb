import unittest  # Importa el módulo unittest para realizar pruebas unitarias.
from Model.review import Review  # Importa la clase Review del módulo model.review.
from Model.user import User  # Importa la clase User del módulo model.user.
from Model.place import Place  # Importa la clase Place del módulo model.place.
from Model.city import City  # Importa la clase City del módulo model.city.
from Model.country import Country  # Importa la clase Country del módulo model.country.
from datetime import datetime

class TestReview(unittest.TestCase):  # Define la clase de pruebas para Review.

    def setUp(self):
        # Inicializa datos comunes para las pruebas
        self.user = User("reviewer@example.com", "password", "Reviewer", "User")  # Crea un usuario revisor.
        self.country = Country(name="Sample Country", code="SC")  # Crea un país.
        self.city = City(name="Sample City", country=self.country)  # Crea una ciudad.
        self.place = Place(
            name="Sample Place",
            description="A sample place",
            address="123 Sample St",
            city=self.city,
            latitude=10.0,
            longitude=20.0,
            host=self.user,
            number_of_rooms=3,
            number_of_bathrooms=2,
            price_per_night=100.0,
            max_guests=4
        )  # Crea un lugar.

    def test_create_review(self):
        # Prueba la creación de una reseña
        review = Review(user=self.user, place=self.place, text="Great place!", rating=5)
        self.assertEqual(review.user, self.user)  # Verifica que el usuario sea el esperado.
        self.assertEqual(review.place, self.place)  # Verifica que el lugar sea el esperado.
        self.assertEqual(review.text, "Great place!")  # Verifica que el texto sea el esperado.
        self.assertEqual(review.rating, 5)  # Verifica que la calificación sea la esperada.
        self.assertIsNotNone(review.id)  # Verifica que el id no sea None.
        self.assertIsNotNone(review.created_at)  # Verifica que la fecha de creación no sea None.
        self.assertIsNotNone(review.updated_at)  # Verifica que la fecha de actualización no sea None.

    def test_update_review(self):
        # Prueba la actualización de una reseña
        review = Review(user=self.user, place=self.place, text="Great place!", rating=5)
        review.update(text="Updated review", rating=4)  # Actualiza el texto y la calificación de la reseña.
        self.assertEqual(review.text, "Updated review")  # Verifica que el texto sea el esperado.
        self.assertEqual(review.rating, 4)  # Verifica que la calificación sea la esperada.
        self.assertNotEqual(review.updated_at, review.created_at)  # Verifica que la fecha de actualización sea diferente a la fecha de creación.

    def test_no_duplicate_reviews_on_same_day(self):
        # Prueba que no se puedan crear reseñas duplicadas en el mismo día
        review1 = Review(user=self.user, place=self.place, text="Great place!", rating=5)
        review1.save_to_json()
        with self.assertRaises(ValueError):  # Verifica que se lance un error al intentar crear una reseña duplicada el mismo día.
            review2 = Review(user=self.user, place=self.place, text="Another review", rating=4)
            review2.save_to_json()

if __name__ == '__main__':
    unittest.main()  # Ejecuta las pruebas.
