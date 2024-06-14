""" lugares / places"""


import uuid
from datetime import datetime

class Place:
    """ clase de lugar/ place"""
    def __init__(self, name, description,amenities, address, city, latitude, longitude, host, number_of_rooms, number_of_bathrooms, price_per_night, max_guests):
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
        self.amenities = amenities
        self.reviews = []

    def add_review(self, review):
        """review del lugar/ place review"""
        self.reviews.append(review)

    def calculate_total_price(self, number_of_nights):
        """calcula precio por noche / calculates prices p.n"""
        return self.price_per_night * number_of_nights

    def list_amenities(self):
        """Lista de amenities / list of amenities"""
        return self.amenities

    def check_availability(self, start_date, end_date):
        """ avilities por noche / checks the avility for the dates"""
        pass

    def list_reviews(self):
        """reviews"""
        return self.reviews

    def set_number_of_guests(self, number):
        """numero de visitantes / nuber of staying guest"""
        self.max_guests = number

    def add_description(self, description):
        """añade descripcion /add description."""
        self.description = description

    def set_number_of_rooms(self, number):
        """numero de habitaciones / number of romms """
        self.number_of_rooms = number

    def set_location(self, latitude, longitude):
        """Locacion / location."""
        self.latitude = latitude
        self.longitude = longitude

    def add_amenity(self, amenities):
        """añade una amenity / adds amenity."""
        self.amenity_ids.append(amenities)

    def toggle_availability(self):
        """juega con el availability de el room / toogle availability"""
        pass

    def get_description(self):
        """toma la descripcion del lugar / gets de description of the place"""
        return self.description

    def get_location(self):
        """Toma la locacion del lugar /Gets the location of the place"""
        return self.latitude, self.longitude

    def update_place_data(self, new_data):
        """update a la data / updates data"""
        for key, value in new_data.items():
            setattr(self, key, value)

    def delete_amenity(self, amenities):
        """borra amenity del lugar por el ID / deletes amenities from place ID"""
        if amenities in self.amenities:
            self.amenities.remove(amenities)

    def dict(self):
        """diccionario / dict"""
        return {
            'place_id': self.place_id,
            'name': self.name,
            'description': self.description,
            'address': self.address,
            'city_id': self.city_id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'host_id': self.host_id,
            'number_of_rooms': self.number_of_rooms,
            'number_of_bathrooms': self.number_of_bathrooms,
            'price_per_night': self.price_per_night,
            'max_guests': self.max_guests,
            'amenity_ids': self.amenities,
            'reviews': self.reviews
        }