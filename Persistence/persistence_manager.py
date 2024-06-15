from abc import ABC, abstractmethod  # Importa la clase ABC y el método abstracto

class IPersistenceManager(ABC):
    """Interfaz para definir métodos del administrador de persistencia."""

    @abstractmethod
    def save(self, entity):
       # Guarda una entidad.
        pass

    @abstractmethod
    def get(self, entity_id):
       # Obtiene una entidad por su ID.
        pass

    @abstractmethod
    def update(self, entity_id, new_data):
        # Actualiza una entidad existente.
        pass

    @abstractmethod
    def delete(self, entity_id):
       # Elimina una entidad existente.
        pass

    @abstractmethod
    def get_all(self):
       # Obtiene todas las entidades.
        pass