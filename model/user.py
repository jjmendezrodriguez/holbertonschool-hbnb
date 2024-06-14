"""usuarios / users."""

import uuid
from datetime import datetime


class User:
    """Clase de usuario / user  class"""
    def __init__(self, username, email, password):
        """ crea el user ID / creates user ID"""
        self.user_id = str(uuid.uuid4())
        self.username = username
        self.email = email
        """ crea password para el user / creates password for the user"""
        self.password = password
        """ el tiempo de creacion / creation time"""
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.reviews = []

    def add_review(self, review):
        """añade un review / adds review"""
        self.reviews.append(review)

    def list_reviews(self):
        """lista de reviews / list of reviews."""
        return self.reviews

    def update_user_data(self, new_data):
        """ da update a la data user / updates data user"""
        for key, value in new_data.items():
            setattr(self, key, value)

    def check_password(self, password):
        """chequea si el password esta bien / checks is password is TRUE"""
        return self.password == password

    def dict(self):
        """retorna como diccionario / returns data as dictionary"""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            # Convert datetime to ISO 8601 format
            'created_at': self.created_at.isoformat(),
            # Convert datetime to ISO 8601 format
            'updated_at': self.updated_at.isoformat(),
            'reviews': self.reviews
        }