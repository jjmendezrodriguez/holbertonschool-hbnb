from flask import Flask
from flask_restx import Api

app = Flask(__name__)
api = Api(app, version='1.0', title='Comprehensive API', description='API to manage countries, cities, amenities, places, reviews, and users')

from .country_api import ns as country_namespace
from .city_api import ns as city_namespace
from .amenity_api import ns as amenity_namespace
from .place_api import ns as place_namespace
from .review_api import ns as review_namespace
from .user_api import ns as user_namespace

api.add_namespace(country_namespace)
api.add_namespace(city_namespace)
api.add_namespace(amenity_namespace)
api.add_namespace(place_namespace)
api.add_namespace(review_namespace)
api.add_namespace(user_namespace)
