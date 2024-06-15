""" modelo de las ciudades/ model cities"""


import uuid
from datetime import datetime

class City:
    """clase - ciudad"""
    def __init__(self, name, country_id):
        """ creando su ID / creating ID"""
        self.city_id = str(uuid.uuid4())
        self.name = name
        self.country_id = country_id
        """ tiempo de creación y update / time of creation and update"""
        self.created_at = datetime.now()  # Record creation timestamp
        self.updated_at = datetime.now()  # Record update timestamp

    def dict(self):
        """retorna ciudad como diccionario/ city as  dictionary."""
        return {
            'city_id': self.city_id,
            'name': self.name,
            'country_id': self.country_id,
            """ creacion y update en ISOformat"""
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }