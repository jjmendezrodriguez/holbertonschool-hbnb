""" amenidades / amenitys"""


import uuid
from datetime import datetime

class Amenity:
    def __init__(self, name, description):
        """ identificacion"""
        self.amenity_id = str(uuid.uuid4())
        self.name = name
        self.description = description
        """tiempo de creacion"""
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def dict(self):
        """ retorna amenity como diccionario"""
        return {
            'amenity_id': self.amenity_id,
            'name': self.name,
            """ convertir el tiempo en ISOformat"""
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }