""" Paises / countrys """


import uuid
from datetime import datetime

class Country:
    def __init__(self, name):
        """ creando el ID/ creating ID"""
        self.country_id = str(uuid.uuid4())
        self.name = name
        """ tiempo de creacion / creation time"""
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def dict(self):
        """retorna diccionario / returns dictionary"""
        return {
            'country_id': self.country_id,
            'name': self.name,
            """ convertir date a isoformat / converting date iso format"""
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }