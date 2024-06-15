from Persistence.amenity_repo import AmenityRepo  # Importa el repositorio de comodidades
from Persistence.city_repo import CityRepo  # Importa el repositorio de ciudades
from Persistence.country_repo import CountryRepo  # Importa el repositorio de países
from Persistence.place_repo import PlaceRepo  # Importa el repositorio de lugares
from Persistence.review_repo import ReviewRepo  # Importa el repositorio de reseñas
from Persistence.user_repo import UserRepo  # Importa el repositorio de usuarios
from Model.amenity import Amenity  # Importa el modelo de comodidades
from Model.city import City  # Importa el modelo de ciudades
from Model.country import Country  # Importa el modelo de países
from Model.place import Place  # Importa el modelo de lugares
from Model.review import Review  # Importa el modelo de reseñas
from Model.user import User  # Importa el modelo de usuarios

class DataManager:
    """Clase para gestionar operaciones CRUD para varias entidades."""
    def __init__(self):
        self.place_repo = PlaceRepo()  # Inicializa el repositorio de lugares
        self.user_repo = UserRepo()  # Inicializa el repositorio de usuarios
        self.review_repo = ReviewRepo()  # Inicializa el repositorio de reseñas
        self.amenity_repo = AmenityRepo()  # Inicializa el repositorio de comodidades
        self.country_repo = CountryRepo()  # Inicializa el repositorio de países
        self.city_repo = CityRepo()  # Inicializa el repositorio de ciudades

    # Métodos para Place
    def save_place(self, place_data):
        place = Place(**place_data)
        self.place_repository.save(place)
        return place.place_id

    def get_place(self, place_id):
        return self.place_repository.get(place_id)

    def update_place(self, place_id, new_data):
        return self.place_repository.update(place_id, new_data)

    def delete_place(self, place_id):
        return self.place_repository.delete(place_id)

    def get_all_places(self):
        return self.place_repository.get_all()

    # Métodos para User
    def save_user(self, user_data):
        user = User(**user_data)
        self.user_repository.save(user)
        return user.user_id

    def get_user(self, user_id):
        return self.user_repository.get(user_id)

    def update_user(self, user_id, new_data):
        return self.user_repository.update(user_id, new_data)

    def delete_user(self, user_id):
        return self.user_repository.delete(user_id)

    def get_all_users(self):
        return self.user_repository.get_all()

    # Métodos para Review
    def save_review(self, review_data):
        review = Review(**review_data)
        self.review_repository.save(review)
        return review.review_id

    def get_review(self, review_id):
        return self.review_repository.get(review_id)

    def update_review(self, review_id, new_data):
        return self.review_repository.update(review_id, new_data)

    def delete_review(self, review_id):
        return self.review_repository.delete(review_id)

    def get_all_reviews(self):
        return self.review_repository.get_all()

    # Métodos para Amenity
    def save_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repository.save(amenity)
        return amenity.amenity_id

    def get_amenity(self, amenity_id):
        return self.amenity_repository.get(amenity_id)

    def update_amenity(self, amenity_id, new_data):
        return self.amenity_repository.update(amenity_id, new_data)

    def delete_amenity(self, amenity_id):
        return self.amenity_repository.delete(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repository.get_all()

    # Métodos para Country
    def save_country(self, country_data):
        country = Country(**country_data)
        self.country_repository.save(country)
        return country.country_id

    def get_country(self, country_id):
        return self.country_repository.get(country_id)

    def update_country(self, country_id, new_data):
        return self.country_repository.update(country_id, new_data)

    def delete_country(self, country_id):
        return self.country_repository.delete(country_id)

    def get_all_countries(self):
        return self.country_repository.get_all()

    # Métodos para City
    def save_city(self, city_data):
        city = City(**city_data)
        self.city_repository.save(city)
        return city.city_id

    def get_city(self, city_id):
        return self.city_repository.get(city_id)

    def update_city(self, city_id, new_data):
        return self.city_repository.update(city_id, new_data)

    def delete_city(self, city_id):
        return self.city_repository.delete(city_id)

    def get_all_cities(self):
        return self.city_repository.get_all()