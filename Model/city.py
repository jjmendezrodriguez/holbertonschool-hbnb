import uuid
from datetime import datetime
import json
import os

class City:  # Define la clase City.
    def __init__(self, name, country):
        self.id = str(uuid.uuid4())  # Genera un UUID único para la ciudad.
        self.name = name  # Asigna el nombre de la ciudad.
        self.country = country  # Asigna el país donde se encuentra la ciudad.
        self.created_at = datetime.now()  # Asigna la fecha y hora actuales al crear la ciudad.
        self.updated_at = datetime.now()  # Asigna la fecha y hora actuales como la última actualización.
        self.places = []  # Inicializa una lista vacía para los lugares asociados a la ciudad.

    def update(self, **kwargs):  # Método para actualizar los atributos de la ciudad.
        for key, value in kwargs.items():  # Itera sobre los argumentos proporcionados.
            setattr(self, key, value)  # Actualiza el atributo correspondiente con el nuevo valor.
        self.updated_at = datetime.now()  # Actualiza la fecha y hora de la última actualización.

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "country": self.country.name if self.country else None,  # Asume que country es un objeto con atributo name
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "places": [place.to_dict() for place in self.places]  # Convierte cada lugar a diccionario
        }

    """ Verifica si ya existe una ciudad con el mismo nombre y país en el archivo JSON."""
    @staticmethod
    def exists(name, country, directory='data', filename='cities.json'):
        filepath = os.path.join(directory, filename)
        if not os.path.exists(filepath):
            return False
        with open(filepath, 'r') as f:
            cities = json.load(f)
            for city in cities:
                if city['name'] == name and city['country'] == country.name:
                    return True
        return False
    
    """ Llama al método exists antes de guardar la ciudad para verificar duplicados.
        Si un duplicado es encontrado, lanza un ValueError. Si no se encuentra un
        duplicado, actualiza el timestamp updated_at, verifica y crea el directorio
        si es necesario, carga las ciudades existentes, añade la nueva ciudad y
        guarda todo de nuevo en el archivo JSON. """
    def save_to_json(self, directory='data', filename='cities.json'):
        if City.exists(self.name, self.country, directory, filename):
            raise ValueError("A city with this name and country already exists.")
        
        self.updated_at = datetime.now()
        if not os.path.exists(directory):
            os.makedirs(directory)
        filepath = os.path.join(directory, filename)
        
        cities = []
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                cities = json.load(f)

        cities.append(self.to_dict())

        with open(filepath, 'w') as f:
            json.dump(cities, f, indent=4)

    def __repr__(self):
        return f'<City {self.name}>'
