import uuid
from datetime import datetime

class Review:
    _reviews = []

    def __init__(self, user_id, place_id, rating, comment):
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.place_id = place_id
        self.rating = rating
        self.comment = comment
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        self.updated_at = datetime.now()
        # Add logic to save the review to persistence layer

    def __repr__(self):
        return f'<Review {self.comment[:20]}>'