import uuid
from datetime import datetime
import json
import os

class Amenity:  # Define la clase Amenity.
    def __init__(self, name, description):
        self.id = str(uuid.uuid4())  # Genera un UUID único para la comodidad.
        self.name = name  # Asigna el nombre de la comodidad.
        self.description = description  # Asigna la descripción de la comodidad.
        self.created_at = datetime.now()  # Asigna la fecha y hora actuales al crear la comodidad.
        self.updated_at = datetime.now()  # Asigna la fecha y hora actuales como la última actualización.

    def update(self, **kwargs):  # Método para actualizar los atributos de la comodidad.
        for key, value in kwargs.items():  # Itera sobre los argumentos proporcionados.
            setattr(self, key, value)  # Actualiza el atributo correspondiente con el nuevo valor.
        self.updated_at = datetime.now()  # Actualiza la fecha y hora de la última actualización.

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    """ Verifica si ya existe una comodidad con el mismo
        nombre en el archivo JSON.filepath =
        os.path.join(directory, filename): Construye la 
        ruta completa del archivo JSON.
        Si el archivo no existe, devuelve False.
        Abre el archivo en modo lectura y carga el contenido
        del archivo JSON en una lista de diccionarios.
        Itera sobre cada comodidad en la lista y verifica si el name coincide."""
    @staticmethod
    def exists(name, directory='data', filename='amenities.json'):
        filepath = os.path.join(directory, filename)
        if not os.path.exists(filepath):
            return False
        with open(filepath, 'r') as f:
            amenities = json.load(f)
            for amenity in amenities:
                if amenity['name'] == name:
                    return True
        return False

    """ Llama al método exists antes de guardar la comodidad para
    verificar duplicados. Si un duplicado es encontrado, lanza un ValueError.
Si no se encuentra un duplicado, actualiza el timestamp updated_at, verifica
y crea el directorio si es necesario, carga las comodidades existentes, añade
la nueva comodidad y guarda todo de nuevo en el archivo JSON."""
    def save_to_json(self, directory='data', filename='amenities.json'):
        if Amenity.exists(self.name, directory, filename):
            raise ValueError("An amenity with this name already exists.")
        
        self.updated_at = datetime.now()
        if not os.path.exists(directory):
            os.makedirs(directory)
        filepath = os.path.join(directory, filename)
        
        amenities = []
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                amenities = json.load(f)

        amenities.append(self.to_dict())

        with open(filepath, 'w') as f:
            json.dump(amenities, f, indent=4)

    def __repr__(self):
        return f'<Amenity {self.name}>'
