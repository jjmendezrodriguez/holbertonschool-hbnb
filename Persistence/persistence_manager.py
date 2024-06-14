from abc import ABC, abstractmethod  # Importa la clase ABC y el método abstracto

class IPersistenceManager(ABC):
    """Interfaz para definir métodos del administrador de persistencia."""

    @abstractmethod
    def save(self, entity):
        """
        Guarda una entidad.

        Args:
            entity (object): La entidad que se va a guardar.
        """
        pass

    @abstractmethod
    def get(self, entity_id):
        """
        Obtiene una entidad por su ID.

        Args:
            entity_id (str/int): El identificador único de la entidad.

        Returns:
            object: El objeto de la entidad si se encuentra, de lo contrario None.
        """
        pass

    @abstractmethod
    def update(self, entity_id, new_data):
        """
        Actualiza una entidad existente.

        Args:
            entity_id (str/int): El identificador único de la entidad que se actualizará.
            new_data (dict): Un diccionario que contiene los nuevos datos para la entidad.

        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        pass

    @abstractmethod
    def delete(self, entity_id):
        """
        Elimina una entidad existente.

        Args:
            entity_id (str/int): El identificador único de la entidad que se eliminará.

        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario.
        """
        pass

    @abstractmethod
    def get_all(self):
        """
        Obtiene todas las entidades.

        Returns:
            list: Una lista de todos los objetos de entidad.
        """
        pass
