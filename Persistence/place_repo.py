from Model.place import Place
from Persistence.persistence_manager import IPersistenceManager


class PlaceRepo(IPersistenceManager):
    """Clase para gestionar la persistencia de lugares."""

    def __init__(self):
        """Inicializa PlaceRepo con un diccionario vacío
        y un contador next_id."""
        self.places = {}
        self.next_id = 1

    def save(self, place):
        """
        Guarda un lugar.
        """
        if not hasattr(place, 'place_id'):
            place.place_id = self.next_id
            self.next_id += 1
        self.places[place.place_id] = place

    def get(self, place_id):
        """
        Obtiene un lugar por su ID.
        """
        return self.places.get(place_id)

    def get_all(self):
        """
        Obtiene todos los lugares.
        """
        return list(self.places.values())

    def update(self, place_id, new_place_data):
        """
        Actualiza un lugar existente.
        """
        if place_id in self.places:
            place = self.places[place_id]
            place.update_place_data(new_place_data)
            self.save(place)
            return True
        return False

    def delete(self, place_id):
        """
        Elimina un lugar existente.
        """
        if place_id in self.places:
            del self.places[place_id]
            return True
        return False
