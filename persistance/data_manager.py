from persistance.persistence_manager import IPersistenceManager
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models.country import Country
from models.city import City

class DataManager(IPersistenceManager):
    def __init__(self):
        self.storage = {
            'User': {},
            'Place': {},
            'Review': {},
            'Amenity': {},
            'Country': {},
            'City': {}
        }

    def save(self, entity):
        entity_type = entity.__class__.__name__
        self.storage[entity_type][entity.id] = entity

    def get(self, entity_id, entity_type):
        return self.storage[entity_type].get(entity_id)

    def update(self, entity):
        entity_type = entity.__class__.__name__
        if entity.id in self.storage[entity_type]:
            self.storage[entity_type][entity.id] = entity

    def delete(self, entity_id, entity_type):
        if entity_id in self.storage[entity_type]:
            del self.storage[entity_type][entity_id]
