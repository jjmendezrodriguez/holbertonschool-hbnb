import uuid 
from datetime import datetime
import json
import os

class Review:  # Define la clase Review.
    def __init__(self, user, place, text, rating):
        self.id = str(uuid.uuid4())  # Genera un UUID único para la reseña.
        self.user = user  # Asigna el usuario que realizó la reseña (objeto User).
        self.place = place  # Asigna el lugar reseñado (objeto Place).
        self.text = text  # Asigna el texto de la reseña.
        self.rating = rating  # Asigna la calificación de la reseña.
        self.created_at = datetime.now()  # Asigna la fecha y hora actuales al crear la reseña.
        self.updated_at = datetime.now()  # Asigna la fecha y hora actuales como la última actualización.

    def update(self, **kwargs):  # Método para actualizar los atributos de la reseña.
        for key, value in kwargs.items():  # Itera sobre los argumentos proporcionados.
            setattr(self, key, value)  # Actualiza el atributo correspondiente con el nuevo valor.
        self.updated_at = datetime.now()  # Actualiza la fecha y hora de la última actualización.

    def to_dict(self):
        return {
            "id": self.id,
            "user": self.user.email if self.user else None,  # Asume que user es un objeto User
            "place": self.place.name if self.place else None,  # Asume que place es un objeto Place
            "text": self.text,
            "rating": self.rating,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    """ Verifica si ya existe una reseña del mismo usuario para el mismo
    lugar en la misma fecha en el archivo JSON. Convierte la fecha de creación
    de la reseña desde el formato ISO a un objeto date. Compara el usuario, el
    lugar y la fecha para determinar si ya existe una reseña para el mismo día."""
    @staticmethod 
    def exists(user, place, date, directory='data', filename='reviews.json'):
        filepath = os.path.join(directory, filename)
        if not os.path.exists(filepath):
            return False
        with open(filepath, 'r') as f:
            reviews = json.load(f)
            for review in reviews:
                review_date = datetime.fromisoformat(review['created_at']).date()
                if review['user'] == user.email and review['place'] == place.name and review_date == date:
                    return True
        return False
    """ para guardar el review lo revisa antes con el criterio de def exists"""
    def save_to_json(self, directory='data', filename='reviews.json'):
        today = datetime.now().date()
        if Review.exists(self.user, self.place, today, directory, filename):
            raise ValueError("A review by this user for this place already exists today.")
        
        self.updated_at = datetime.now()
        if not os.path.exists(directory):
            os.makedirs(directory)
        filepath = os.path.join(directory, filename)
        
        reviews = []
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                reviews = json.load(f)

        reviews.append(self.to_dict())

        with open(filepath, 'w') as f:
            json.dump(reviews, f, indent=4)

    def __repr__(self):
        return f'<Review {self.id}>'
