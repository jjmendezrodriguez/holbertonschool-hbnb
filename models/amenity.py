import uuid
from datetime import datetime

class Amenity:
    def __init__(self, name):
        self.id = str(uuid.uuid4())
        self.name = name
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        self.updated_at = datetime.now()
        # Add logic to save the amenity to persistence layer

    def __repr__(self):
        return f'<Amenity {self.name}>'
    