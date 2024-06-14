import uuid
from datetime import datetime

class Review:
    def __init__(self, user, place, text, rating):
        self.id = str(uuid.uuid4())
        self.user = user
        self.place = place
        self.text = text
        self.rating = rating
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
