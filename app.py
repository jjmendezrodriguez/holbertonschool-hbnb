from flask import Flask
from flask_restx import Api
from API.country_api import ns as country_namespace
from API.city_api import ns as city_namespace
from API.amenity_api import ns as amenity_namespace
from API.place_api import ns as place_namespace
from API.review_api import ns as review_namespace
from API.user_api import ns as user_namespace

app = Flask(__name__)
api = Api(app, version='1.0', title='Comprehensive API', description='API to manage countries, cities, amenities, places, reviews, and users')

api.add_namespace(country_namespace)
api.add_namespace(city_namespace)
api.add_namespace(amenity_namespace)
api.add_namespace(place_namespace)
api.add_namespace(review_namespace)
api.add_namespace(user_namespace)

import os

if __name__ == '__main__':
    app.run(debug=True)
