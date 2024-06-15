from Model.review import Review
from Persistence.persistence_manager import IPersistenceManager


class ReviewRepo(IPersistenceManager):
    """Clase para gestionar la persistencia de reseñas."""

    def __init__(self):
       # Inicializa ReviewRepo con un diccionario vacío
       # y un contador next_id.
        self.reviews = {}
        self.next_id = 1

    def save(self, review):
       # Guarda una reseña.

       # Si la reseña no tiene un review_id, asigna un nuevo ID único.
       # Luego, la reseña se almacena en el diccionario de reseñas.
        
        if not hasattr(review, 'review_id'):
            review.review_id = self.next_id
            self.next_id += 1
        self.reviews[review.review_id] = review

    def get(self, review_id):
       # Obtiene una reseña por su ID.
        
        return self.reviews.get(review_id)

    def get_all(self):
       # Obtiene todas las reseñas.
        
        return list(self.reviews.values())

    def update(self, review_id, new_review_data):
       # Actualiza una reseña existente.
        
        if review_id in self.reviews:
            review = self.reviews[review_id]
            for key, value in new_review_data.items():
                setattr(review, key, value)
            self.save(review)
            return True
        return False

    def delete(self, review_id):
       # Elimina una reseña existente.
        
        if review_id in self.reviews:
            del self.reviews[review_id]
            return True
        return False