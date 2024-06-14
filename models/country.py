import uuid
from datetime import datetime

class Country:
    def __init__(self, code, name):
        self.code = code
        self.name = name
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        self.updated_at = datetime.now()
        # Add logic to save the country to persistence layer

    def __repr__(self):
        return f'<Country {self.name}>'