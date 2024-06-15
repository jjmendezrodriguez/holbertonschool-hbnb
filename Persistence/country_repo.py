from Model.country import Country
from Persistence.persistence_manager import IPersistenceManager


class CountryRepo(IPersistenceManager):
    """Clase para gestionar la persistencia de países."""

    def __init__(self):
       # Inicializa CountryRepo con un diccionario vacío
       # y un contador next_id.
        self.countries = {}
        self.next_id = 1

    def save(self, country):
       # Guarda un país.
        
        if not hasattr(country, 'country_id'):
            country.country_id = self.next_id
            self.next_id += 1
        self.countries[country.country_id] = country

    def get(self, country_id):
       # Obtiene un país por su ID.
        
        return self.countries.get(country_id)

    def get_all(self):
       # Obtiene todos los países.
        
        return list(self.countries.values())

    def update(self, country_id, new_country_data):
       # Actualiza un país existente.
        
        if country_id in self.countries:
            country = self.countries[country_id]
            for key, value in new_country_data.items():
                setattr(country, key, value)
            self.save(country)
            return True
        return False

    def delete(self, country_id):
       # Elimina un país existente.
    
        if country_id in self.countries:
            del self.countries[country_id]
            return True
        return False