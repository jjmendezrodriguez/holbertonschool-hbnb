""" reviews"""

import uuid
from datetime import datetime

class Review:
    """clase para los reviews / class for review"""
    def __init__(self, user_id, place_id, rating, comment):
        """ genera el id / creates ID"""
        self.review_id = str(uuid.uuid4())
        self.user_id = user_id
        self.place_id = place_id
        self.rating = rating
        self.comment = comment
        """ tiempo de creacion y update / time of creation and update"""
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def dict(self):
        """retorna data como diccionario / returns the data as dictionary"""
        return {
            'review_id': self.review_id,
            'user_id': self.user_id,
            'place_id': self.place_id,
            'rating': self.rating,
            'comment': self.comment,
            """ convierte el date en ISOformat / converts the date time as ISO format"""
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }