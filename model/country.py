import uuid
from datetime import datetime

class Country:
    def __init__(self, name, code):
        self.id = str(uuid.uuid4())
        self.name = name
        self.code = code
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.cities = []
