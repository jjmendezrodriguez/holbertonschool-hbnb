import uuid
from datetime import datetime
import json
import os
from flask import Flask, request

class User:
    _emails = {} # revisa que los email no se puedan repetir si se repiden envia un error.

    """ con esta funcion podemos crear los atributos de los users
        para que sean unicos"""
    def __init__(self, email, password, first_name, last_name):
        if email in User._emails:
            raise ValueError("A user with this email already exists.")
        self.id = str(uuid.uuid4())
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.places = []
        User._emails[email] = self

    """esta funcion ayuda a modificar update la info de los usuario y 
        si se repite te avisa enviando un error"""
    def update(self, email=None, password=None, first_name=None, last_name=None):
        if email and email != self.email:
            if email in User._emails:
                raise ValueError(f"Email {email} is already in use.")
            del User._emails[self.email]
            User._emails[email] = self
            self.email = email
        if password:
            self.password = password
        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name
        self.updated_at = datetime.now()

    """ Convierte el objeto User en un diccionario
        adecuado para la serialización JSON."""
    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "places": self.places
        }

    """ Actualiza la fecha de última modificación.
        Verifica si el directorio data existe y lo crea si es necesario.
        Construye la ruta del archivo y guarda los datos en formato JSON."""
    def save_to_json(self, directory='data', filename='users.json'):
        self.updated_at = datetime.now()
        User._emails[self.email] = self
        if not os.path.exists(directory):
            os.makedirs(directory)
        filepath = os.path.join(directory, filename)
        with open(filepath, 'w') as f:
            json.dump([user.to_dict() for user in User._emails.values()], f, indent=4)

    """ Devuelve una cadena que contiene el nombre de la clase (User) y el email del usuario.
        Esto facilita la identificación de los objetos User al imprimirlos."""
    def __repr__(self):
        return f'<User {self.email}>'
