import json
import os
from datetime import datetime
from persistence_manager import IPersistenceManager

class DataManager(IPersistenceManager):
    
    def __init__(self, storage_directory="data"):
        self.storage_directory = storage_directory
        if not os.path.exists(self.storage_directory):
            os.makedirs(self.storage_directory)

    def _get_file_path(self, entity_type):
        return os.path.join(self.storage_directory, f"{entity_type}.json")

    def save(self, entity):
        entity_type = type(entity).__name__.lower()
        file_path = self._get_file_path(entity_type)

        try:
            with open(file_path, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []

        data.append(entity.to_dict())

        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

    def get(self, entity_id, entity_type):
        file_path = self._get_file_path(entity_type.lower())

        try:
            with open(file_path, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            return None

        for entity in data:
            if entity["id"] == str(entity_id):
                return entity
        return None

    def get_all(self, entity_type):
        file_path = self._get_file_path(entity_type.lower())

        try:
            with open(file_path, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            return []

        return data

    def update(self, entity):
        entity_type = type(entity).__name__.lower()
        file_path = self._get_file_path(entity_type)

        try:
            with open(file_path, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            return

        for idx, stored_entity in enumerate(data):
            if stored_entity["id"] == str(entity.id):
                data[idx] = entity.to_dict()

        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

    def delete(self, entity_id, entity_type):
        file_path = self._get_file_path(entity_type.lower())

        try:
            with open(file_path, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            return

        data = [entity for entity in data if entity["id"] != str(entity_id)]

        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
