from abc import ABC, abstractmethod  # Importa ABC y abstractmethod del módulo abc para crear clases abstractas.

class IPersistenceManager(ABC):  # Define una clase abstracta llamada IPersistenceManager que hereda de ABC (Abstract Base Class).
    
    @abstractmethod  # Declara que save es un método abstracto, que debe ser implementado por cualquier clase que herede de IPersistenceManager.
    def save(self, entity):
        pass  # pass indica que no hay implementación en este punto.

    @abstractmethod  # Declara que get es un método abstracto.
    def get(self, entity_id, entity_type):
        pass  # No hay implementación, debe ser definida por la clase derivada.

    @abstractmethod  # Declara que update es un método abstracto.
    def update(self, entity):
        pass  # No hay implementación, debe ser definida por la clase derivada.

    @abstractmethod  # Declara que delete es un método abstracto.
    def delete(self, entity_id, entity_type):
        pass  # No hay implementación, debe ser definida por la clase derivada.
