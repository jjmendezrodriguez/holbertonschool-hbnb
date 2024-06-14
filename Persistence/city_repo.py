import uuid
from Model.city import City
from Persistence.persistence_manager import IPersistenceManager


class CityRepo(IPersistenceManager):
    """Clase para gestionar la persistencia de ciudades."""

    def __init__(self):
        """Inicializa CityRepo con un diccionario vacío
        para almacenar ciudades.
        """
        self.cities = {}

    def save(self, city):
        """
        Guarda una ciudad.
        """
        if not hasattr(city, 'city_id') or city.city_id is None:
            city.city_id = str(uuid.uuid4())
        self.cities[city.city_id] = city

    def get(self, city_id):
        """
        Obtiene una ciudad por su ID.
        """
        return self.cities.get(city_id)

    def get_all(self):
        """
        Obtiene todas las ciudades.
        """
        return list(self.cities.values())

    def update(self, city_id, new_city_data):
        """
        Actualiza una ciudad existente.
        """
        if city_id in self.cities:
            city = self.cities[city_id]
            for key, value in new_city_data.items():
                setattr(city, key, value)
            self.save(city)
            return True
        return False

    def delete(self, city_id):
        """
        Elimina una ciudad existente.
        """
        if city_id in self.cities:
            del self.cities[city_id]
            return True
        return False
