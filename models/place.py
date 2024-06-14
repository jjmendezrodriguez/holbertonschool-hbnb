import uuid
from datetime import datetime

class Place:
    def __init__(self, name, description, address, city_id, latitude, longitude, host_id, number_of_rooms, number_of_bathrooms, price_per_night, max_guests):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.address = address
        self.city_id = city_id
        self.latitude = latitude
        self.longitude = longitude
        self.host_id = host_id
        self.number_of_rooms = number_of_rooms
        self.number_of_bathrooms = number_of_bathrooms
        self.price_per_night = price_per_night
        self.max_guests = max_guests
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.amenities = []

    def add_amenity(self, amenity):
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def save(self):
        self.updated_at = datetime.now()
        # Add logic to save the place to persistence layer
    
    def set_host(self, host_id):
        if self.host_id:
            raise ValueError("This place already has a host.")
        self.host_id = host_id

    def __repr__(self):
        return f'<Place {self.name}>'