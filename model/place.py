import uuid
from datetime import datetime

class Place:
    def __init__(self, name, description, address, city, latitude, longitude, host, number_of_rooms, number_of_bathrooms, price_per_night, max_guests):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.address = address
        self.city = city
        self.latitude = latitude
        self.longitude = longitude
        self.host = host
        self.number_of_rooms = number_of_rooms
        self.number_of_bathrooms = number_of_bathrooms
        self.price_per_night = price_per_night
        self.max_guests = max_guests
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.amenities = []
        self.reviews = []
