""" Paises / countrys """


import uuid
from datetime import datetime

class Country:
    def __init__(self, name, code):
        """ creando el ID/ creating ID"""
        self.id = str(uuid.uuid4())
        self.name = name
        self.code = code
        """ tiempo de creacion / creation time"""
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.cities = []

    def dict(self):
        """retorna diccionario / returns dictionary"""
        return {
            'country_id': self.country_id,
            'name': self.name,
            """ convertir date a isoformat / converting date iso format"""
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }