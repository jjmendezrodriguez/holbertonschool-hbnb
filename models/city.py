import uuid
from datetime import datetime

class City:
    def __init__(self, name, country_code):
        self.id = str(uuid.uuid4())
        self.name = name
        self.country_code = country_code
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        self.updated_at = datetime.now()
        # Add logic to save the city to persistence layer

    def __repr__(self):
        return f'<City {self.name}>'