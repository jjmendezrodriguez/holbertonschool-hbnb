import uuid
from Model.amenity import Amenity
from Persistence.persistence_manager import IPersistenceManager


class AmenityRepo(IPersistenceManager):
    """Clase para gestionar la persistencia de comodidades."""

    def __init__(self):
        """Inicializa AmenityRepo con un diccionario vacío
        para almacenar comodidades.
        """
        self.amenities = {}

    def save(self, amenity):
        """
        Guarda una comodidad.
        Si la comodidad no tiene un amenity_id,
        se genera un nuevo ID único.
        Luego, la comodidad se almacena en el diccionario de comodidades.
        """
        if not hasattr(amenity, 'amenity_id') or amenity.amenity_id is None:
            amenity.amenity_id = str(uuid.uuid4())
        self.amenities[amenity.amenity_id] = amenity

    def get(self, amenity_id):
        """
        Obtiene una comodidad por su ID.
        """
        return self.amenities.get(amenity_id)

    def get_all(self):
        """
        Obtiene todas las comodidades.
        """
        return list(self.amenities.values())

    def update(self, amenity_id, new_amenity_data):
        """
        Actualiza una comodidad existente.
        """
        if amenity_id in self.amenities:
            amenity = self.amenities[amenity_id]
            for key, value in new_amenity_data.items():
                setattr(amenity, key, value)
            self.save(amenity)
            return True
        return False

    def delete(self, amenity_id):
        """
        Elimina una comodidad existente.
        """
        if amenity_id in self.amenities:
            del self.amenities[amenity_id]
            return True
        return False
