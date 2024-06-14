import uuid
from datetime import datetime
import json
import os

class Country:  # Define la clase Country.
    def __init__(self, name, code):
        self.id = str(uuid.uuid4())  # Genera un UUID único para el país.
        self.code = code  # Asigna el código del país, sus iniciales.
        self.name = name  # Asigna el nombre del país.
        self.created_at = datetime.now()  # Asigna la fecha y hora actuales al crear el país.
        self.updated_at = datetime.now()  # Asigna la fecha y hora actuales como la última actualización.
        self.cities = []  # Inicializa una lista vacía para las ciudades asociadas al país.

    def update(self, **kwargs):  # Método para actualizar los atributos del país.
        for key, value in kwargs.items():  # Itera sobre los argumentos proporcionados.
            setattr(self, key, value)  # Actualiza el atributo correspondiente con el nuevo valor.
        self.updated_at = datetime.now()  # Actualiza la fecha y hora de la última actualización.

    def to_dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "cities": [city.to_dict() for city in self.cities]  # Convierte cada ciudad a diccionario
        }

    """ Verifica si ya existe un país con el mismo nombre y código en el archivo JSON.
        filepath = os.path.join(directory, filename): Construye la ruta completa del
        archivo JSON. Si el archivo no existe, devuelve False. Abre el archivo en 
        modo lectura y carga el contenido del archivo JSON en una lista de diccionarios.
        Itera sobre cada país en la lista y verifica si name y code coinciden."""
    @staticmethod
    def exists(name, code, directory='data', filename='countries.json'):
        filepath = os.path.join(directory, filename)
        if not os.path.exists(filepath):
            return False
        with open(filepath, 'r') as f:
            countries = json.load(f)
            for country in countries:
                if country['name'] == name and country['code'] == code:
                    return True
        return False

    """ Llama al método exists antes de guardar el país para verificar duplicados.
        Si un duplicado es encontrado, lanza un ValueError. Si no se encuentra un duplicado,
        actualiza el timestamp updated_at, verifica y crea el directorio si es necesario,
        carga los países existentes, añade el nuevo país y guarda todo de nuevo en el archivo JSON."""
    def save_to_json(self, directory='data', filename='countries.json'):
        if Country.exists(self.name, self.code, directory, filename):
            raise ValueError("A country with this name and code already exists.")
        
        self.updated_at = datetime.now()
        if not os.path.exists(directory):
            os.makedirs(directory)
        filepath = os.path.join(directory, filename)
        
        countries = []
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                countries = json.load(f)

        countries.append(self.to_dict())

        with open(filepath, 'w') as f:
            json.dump(countries, f, indent=4)

    def __repr__(self):
        return f'<Country {self.name}>'
