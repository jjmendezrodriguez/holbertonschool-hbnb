import json  # Importa el módulo json para manejar operaciones con JSON.
import os  # Importa el módulo os para operaciones con el sistema de archivos.
from uuid import UUID  # Importa UUID del módulo uuid para manejar identificadores únicos.
from datetime import datetime  # Importa datetime del módulo datetime para manejar fechas y horas.
from Persistence.persistence_manager import IPersistenceManager  # Importa la clase abstracta IPersistenceManager.

class DataManager(IPersistenceManager):  # Define la clase DataManager que implementa la interfaz IPersistenceManager.
    
    def __init__(self, storage_directory="data"):  # Método de inicialización, con storage_directory como parámetro opcional.
        self.storage_directory = storage_directory  # Asigna el directorio de almacenamiento.
        if not os.path.exists(self.storage_directory):  # Verifica si el directorio no existe.
            os.makedirs(self.storage_directory)  # Crea el directorio si no existe.

    def _get_file_path(self, entity_type):  # Método privado para obtener la ruta del archivo basado en el tipo de entidad.
        return os.path.join(self.storage_directory, f"{entity_type}.json")  # Construye la ruta del archivo.

    def save(self, entity):  # Implementación del método save.
        entity_type = type(entity).__name__.lower()  # Obtiene el nombre de la clase de la entidad y lo convierte a minúsculas.
        file_path = self._get_file_path(entity_type)  # Obtiene la ruta del archivo.

        try:
            with open(file_path, "r") as file:  # Intenta abrir el archivo en modo lectura.
                data = json.load(file)  # Carga los datos del archivo.
        except FileNotFoundError:  # Si el archivo no existe, inicializa data como una lista vacía.
            data = []

        data.append(entity.__dict__)  # Añade el diccionario de la entidad a la lista.

        with open(file_path, "w") as file:  # Abre el archivo en modo escritura.
            json.dump(data, file)  # Guarda los datos en el archivo.

    def get(self, entity_id, entity_type):  # Implementación del método get.
        file_path = self._get_file_path(entity_type.lower())  # Obtiene la ruta del archivo.

        try:
            with open(file_path, "r") as file:  # Intenta abrir el archivo en modo lectura.
                data = json.load(file)  # Carga los datos del archivo.
        except FileNotFoundError:  # Si el archivo no existe, retorna None.
            return None

        for entity in data:  # Itera sobre los datos.
            if entity["id"] == str(entity_id):  # Busca la entidad con el id correspondiente.
                return entity  # Retorna la entidad si se encuentra.
        return None  # Retorna None si no se encuentra la entidad.

    def update(self, entity):  # Implementación del método update.
        entity_type = type(entity).__name__.lower()  # Obtiene el nombre de la clase de la entidad y lo convierte a minúsculas.
        file_path = self._get_file_path(entity_type)  # Obtiene la ruta del archivo.

        try:
            with open(file_path, "r") as file:  # Intenta abrir el archivo en modo lectura.
                data = json.load(file)  # Carga los datos del archivo.
        except FileNotFoundError:  # Si el archivo no existe, retorna.
            return

        for idx, stored_entity in enumerate(data):  # Itera sobre los datos con índices.
            if stored_entity["id"] == str(entity.id):  # Busca la entidad con el id correspondiente.
                data[idx] = entity.__dict__  # Actualiza la entidad.

        with open(file_path, "w") as file:  # Abre el archivo en modo escritura.
            json.dump(data, file)  # Guarda los datos en el archivo.

    def delete(self, entity_id, entity_type):  # Implementación del método delete.
        file_path = self._get_file_path(entity_type.lower())  # Obtiene la ruta del archivo.

        try:
            with open(file_path, "r") as file:  # Intenta abrir el archivo en modo lectura.
                data = json.load(file)  # Carga los datos del archivo.
        except FileNotFoundError:  # Si el archivo no existe, retorna.
            return

        data = [entity for entity in data if entity["id"] != str(entity_id)]  # Filtra los datos, excluyendo la entidad con el id correspondiente.

        with open(file_path, "w") as file:  # Abre el archivo en modo escritura.
            json.dump(data, file)  # Guarda los datos en el archivo.
