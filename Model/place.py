import uuid
from datetime import datetime
import json
import os
from flask import Flask, request
"""from flask_restx import # lo trabajamos luego cuando el codigo este final."""

class Place:  # Define la clase Place.
    def __init__(self, name, description, address, city, latitude, longitude, host, number_of_rooms, number_of_bathrooms, price_per_night, max_guests):
        self.id = str(uuid.uuid4())  # Genera un UUID único para el lugar.
        self.name = name  # Asigna el nombre del lugar.
        self.description = description  # Asigna la descripción del lugar.
        self.address = address  # Asigna la dirección del lugar.
        self.city = city  # Asigna la ciudad donde se encuentra el lugar.
        self.latitude = latitude  # Asigna la latitud geográfica del lugar.
        self.longitude = longitude  # Asigna la longitud geográfica del lugar.
        self.host = host  # Asigna el anfitrión del lugar (objeto User).
        self.number_of_rooms = number_of_rooms  # Asigna el número de habitaciones.
        self.number_of_bathrooms = number_of_bathrooms  # Asigna el número de baños.
        self.price_per_night = price_per_night  # Asigna el precio por noche.
        self.max_guests = max_guests  # Asigna el número máximo de huéspedes.
        self.created_at = datetime.now()  # Asigna la fecha y hora actuales al crear el lugar.
        self.updated_at = datetime.now()  # Asigna la fecha y hora actuales como la última actualización.
        self.amenities = []  # Inicializa una lista vacía para las comodidades asociadas al lugar.
        self.reviews = []  # Inicializa una lista vacía para las reseñas asociadas al lugar.

    """para evitar duclicaciones, tienen que ser name y
        address los mismos para que se aplique esta funcion"""
    @staticmethod 
    def exists(name, address, directory='data', filename='places.json'):
        filepath = os.path.join(directory, filename)
        if not os.path.exists(filepath):
            return False
        with open(filepath, 'r') as f:
            places = json.load(f)
            for place in places:
                if place['name'] == name and place['address'] == address:
                    return True
        return False

    """para crear el file json y evita que se repita"""
    def save_to_json(self, directory='data', filename='places.json'):
        if Place.exists(self.name, self.address, directory, filename):
            raise ValueError("A place with this name and address already exists.")
        
        self.updated_at = datetime.now()
        if not os.path.exists(directory):
            os.makedirs(directory)
        filepath = os.path.join(directory, filename)
        
        places = []
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                places = json.load(f)

        places.append(self.to_dict())

        with open(filepath, 'w') as f:
            json.dump(places, f, indent=4)

    def to_dict(self): # info. que envia en formato diccionario.
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "address": self.address,
            "city": self.city,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "host": self.host.email if self.host else None,  # Asume que host es un objeto User
            "number_of_rooms": self.number_of_rooms,
            "number_of_bathrooms": self.number_of_bathrooms,
            "price_per_night": self.price_per_night,
            "max_guests": self.max_guests,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "amenities": self.amenities,
            "reviews": self.reviews
        }

    def __repr__(self):
        return f'<Place {self.name}>'