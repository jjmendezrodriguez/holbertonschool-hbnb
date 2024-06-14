from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from Model.country import Country
from Model.city import City
from Model.amenity import Amenity
from Model.place import Place
from Model.review import Review
from Model.user import User
from Persistence.data_manager import DataManager
from datetime import datetime
import uuid

# Configuración básica de Flask y Flask-Restx
app = Flask(__name__)
api = Api(app, version='1.0', title='Comprehensive API',
          description='API to manage countries, cities, amenities, places, reviews, and users')

ns = api.namespace('api', description='Operations related to various models')

# Inicialización del DataManager
data_manager = DataManager()

# Modelos para la documentación de Swagger
country_model = api.model('Country', {
    'name': fields.String(required=True, description='The country name'),
    'code': fields.String(required=True, description='The country code')
})

city_model = api.model('City', {
    'name': fields.String(required=True, description='The city name'),
    'country_code': fields.String(required=True, description='The ISO country code')
})

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='The amenity name'),
    'description': fields.String(required=True, description='The amenity description')
})

place_model = api.model('Place', {
    'name': fields.String(required=True, description='The place name'),
    'description': fields.String(required=True, description='The place description'),
    'address': fields.String(required=True, description='The place address'),
    'city': fields.String(required=True, description='The city name'),
    'latitude': fields.Float(required=True, description='The latitude of the place'),
    'longitude': fields.Float(required=True, description='The longitude of the place'),
    'host': fields.String(required=True, description='The host user email'),
    'number_of_rooms': fields.Integer(required=True, description='Number of rooms'),
    'number_of_bathrooms': fields.Integer(required=True, description='Number of bathrooms'),
    'price_per_night': fields.Float(required=True, description='Price per night'),
    'max_guests': fields.Integer(required=True, description='Maximum number of guests')
})

review_model = api.model('Review', {
    'user': fields.String(required=True, description='The user email'),
    'place': fields.String(required=True, description='The place name'),
    'text': fields.String(required=True, description='The review text'),
    'rating': fields.Integer(required=True, description='The review rating')
})

user_model = api.model('User', {
    'email': fields.String(required=True, description='The user email'),
    'password': fields.String(required=True, description='The user password'),
    'first_name': fields.String(required=True, description='The user first name'),
    'last_name': fields.String(required=True, description='The user last name')
})

# Endpoints para Country
@ns.route('/countries')
class CountryList(Resource):
    @ns.doc('list_countries')
    @ns.marshal_list_with(country_model)
    def get(self):
        """List all countries"""
        countries = data_manager.get_all('country')
        return countries, 200

@ns.route('/countries/<string:country_code>')
@ns.param('country_code', 'The country identifier')
class CountryResource(Resource):
    @ns.doc('get_country')
    @ns.marshal_with(country_model)
    def get(self, country_code):
        """Fetch a country given its code"""
        country = data_manager.get(country_code, 'country')
        if not country:
            api.abort(404, f"Country {country_code} not found")
        return country, 200

@ns.route('/countries/<string:country_code>/cities')
@ns.param('country_code', 'The country identifier')
class CountryCities(Resource):
    @ns.doc('list_cities_for_country')
    @ns.marshal_list_with(city_model)
    def get(self, country_code):
        """List all cities for a given country"""
        country_code = country_code.upper()
        if not data_manager.get(country_code, 'country'):
            api.abort(404, f"Country {country_code} not found")
        cities = data_manager.get_all('city')
        country_cities = [city for city in cities if city['country_code'] == country_code]
        return country_cities, 200

# Endpoints para City
@ns.route('/cities')
class CityList(Resource):
    @ns.doc('create_city')
    @ns.expect(city_model)
    @ns.marshal_with(city_model, code=201)
    def post(self):
        """Create a new city"""
        data = request.json
        country_code = data['country_code'].upper()
        if not data_manager.get(country_code, 'country'):
            api.abort(400, f"Invalid country code: {country_code}")
        new_city = City(**data)
        data_manager.save(new_city)
        return new_city, 201

    @ns.doc('list_cities')
    @ns.marshal_list_with(city_model)
    def get(self):
        """List all cities"""
        cities = data_manager.get_all('city')
        return cities, 200

@ns.route('/cities/<string:city_id>')
@ns.param('city_id', 'The city identifier')
class CityResource(Resource):
    @ns.doc('get_city')
    @ns.marshal_with(city_model)
    def get(self, city_id):
        """Fetch a city given its ID"""
        city = data_manager.get(city_id, 'city')
        if not city:
            api.abort(404, f"City {city_id} not found")
        return city, 200

    @ns.doc('update_city')
    @ns.expect(city_model)
    @ns.marshal_with(city_model)
    def put(self, city_id):
        """Update a city given its ID"""
        data = request.json
        city = data_manager.get(city_id, 'city')
        if not city:
            api.abort(404, f"City {city_id} not found")
        if 'name' in data:
            city['name'] = data['name']
        if 'country_code' in data:
            country_code = data['country_code'].upper()
            if not data_manager.get(country_code, 'country'):
                api.abort(400, f"Invalid country code: {country_code}")
            city['country_code'] = country_code
        city['updated_at'] = datetime.now().isoformat()
        data_manager.update(City(**city))
        return city, 200

    @ns.doc('delete_city')
    @ns.response(204, 'City deleted')
    def delete(self, city_id):
        """Delete a city given its ID"""
        if not data_manager.get(city_id, 'city'):
            api.abort(404, f"City {city_id} not found")
        data_manager.delete(city_id, 'city')
        return '', 204

# Endpoints para Amenity
@ns.route('/amenities')
class AmenityList(Resource):
    @ns.doc('create_amenity')
    @ns.expect(amenity_model)
    @ns.marshal_with(amenity_model, code=201)
    def post(self):
        """Create a new amenity"""
        data = request.json
        name = data['name']
        if any(amenity['name'] == name for amenity in data_manager.get_all('amenity')):
            api.abort(409, f"Amenity {name} already exists")
        new_amenity = Amenity(**data)
        data_manager.save(new_amenity)
        return new_amenity, 201

    @ns.doc('list_amenities')
    @ns.marshal_list_with(amenity_model)
    def get(self):
        """List all amenities"""
        amenities = data_manager.get_all('amenity')
        return amenities, 200

@ns.route('/amenities/<string:amenity_id>')
@ns.param('amenity_id', 'The amenity identifier')
class AmenityResource(Resource):
    @ns.doc('get_amenity')
    @ns.marshal_with(amenity_model)
    def get(self, amenity_id):
        """Fetch an amenity given its ID"""
        amenity = data_manager.get(amenity_id, 'amenity')
        if not amenity:
            api.abort(404, f"Amenity {amenity_id} not found")
        return amenity, 200

    @ns.doc('update_amenity')
    @ns.expect(amenity_model)
    @ns.marshal_with(amenity_model)
    def put(self, amenity_id):
        """Update an amenity given its ID"""
        data = request.json
        amenity = data_manager.get(amenity_id, 'amenity')
        if not amenity:
            api.abort(404, f"Amenity {amenity_id} not found")
        if 'name' in data:
            if any(a['name'] == data['name'] for a in data_manager.get_all('amenity') if a['id'] != amenity_id):
                api.abort(409, f"Amenity {data['name']} already exists")
            amenity['name'] = data['name']
        if 'description' in data:
            amenity['description'] = data['description']
        amenity['updated_at'] = datetime.now().isoformat()
        data_manager.update(Amenity(**amenity))
        return amenity, 200

    @ns.doc('delete_amenity')
    @ns.response(204, 'Amenity deleted')
    def delete(self, amenity_id):
        """Delete an amenity given its ID"""
        if not data_manager.get(amenity_id, 'amenity'):
            api.abort(404, f"Amenity {amenity_id} not found")
        data_manager.delete(amenity_id, 'amenity')
        return '', 204

# Endpoints para Place
@ns.route('/places')
class PlaceList(Resource):
    @ns.doc('create_place')
    @ns.expect(place_model)
    @ns.marshal_with(place_model, code=201)
    def post(self):
        """Create a new place"""
        data = request.json
        new_place = Place(**data)
        data_manager.save(new_place)
        return new_place, 201

    @ns.doc('list_places')
    @ns.marshal_list_with(place_model)
    def get(self):
        """List all places"""
        places = data_manager.get_all('place')
        return places, 200

@ns.route('/places/<string:place_id>')
@ns.param('place_id', 'The place identifier')
class PlaceResource(Resource):
    @ns.doc('get_place')
    @ns.marshal_with(place_model)
    def get(self, place_id):
        """Fetch a place given its ID"""
        place = data_manager.get(place_id, 'place')
        if not place:
            api.abort(404, f"Place {place_id} not found")
        return place, 200

    @ns.doc('update_place')
    @ns.expect(place_model)
    @ns.marshal_with(place_model)
    def put(self, place_id):
        """Update a place given its ID"""
        data = request.json
        place = data_manager.get(place_id, 'place')
        if not place:
            api.abort(404, f"Place {place_id} not found")
        if 'name' in data:
            place['name'] = data['name']
        if 'description' in data:
            place['description'] = data['description']
        if 'address' in data:
            place['address'] = data['address']
        if 'city' in data:
            place['city'] = data['city']
        if 'latitude' in data:
            place['latitude'] = data['latitude']
        if 'longitude' in data:
            place['longitude'] = data['longitude']
        if 'host' in data:
            place['host'] = data['host']
        if 'number_of_rooms' in data:
            place['number_of_rooms'] = data['number_of_rooms']
        if 'number_of_bathrooms' in data:
            place['number_of_bathrooms'] = data['number_of_bathrooms']
        if 'price_per_night' in data:
            place['price_per_night'] = data['price_per_night']
        if 'max_guests' in data:
            place['max_guests'] = data['max_guests']
        place['updated_at'] = datetime.now().isoformat()
        data_manager.update(Place(**place))
        return place, 200

    @ns.doc('delete_place')
    @ns.response(204, 'Place deleted')
    def delete(self, place_id):
        """Delete a place given its ID"""
        if not data_manager.get(place_id, 'place'):
            api.abort(404, f"Place {place_id} not found")
        data_manager.delete(place_id, 'place')
        return '', 204

# Endpoints para Review
@ns.route('/reviews')
class ReviewList(Resource):
    @ns.doc('create_review')
    @ns.expect(review_model)
    @ns.marshal_with(review_model, code=201)
    def post(self):
        """Create a new review"""
        data = request.json
        new_review = Review(**data)
        data_manager.save(new_review)
        return new_review, 201

    @ns.doc('list_reviews')
    @ns.marshal_list_with(review_model)
    def get(self):
        """List all reviews"""
        reviews = data_manager.get_all('review')
        return reviews, 200

@ns.route('/reviews/<string:review_id>')
@ns.param('review_id', 'The review identifier')
class ReviewResource(Resource):
    @ns.doc('get_review')
    @ns.marshal_with(review_model)
    def get(self, review_id):
        """Fetch a review given its ID"""
        review = data_manager.get(review_id, 'review')
        if not review:
            api.abort(404, f"Review {review_id} not found")
        return review, 200

    @ns.doc('update_review')
    @ns.expect(review_model)
    @ns.marshal_with(review_model)
    def put(self, review_id):
        """Update a review given its ID"""
        data = request.json
        review = data_manager.get(review_id, 'review')
        if not review:
            api.abort(404, f"Review {review_id} not found")
        if 'text' in data:
            review['text'] = data['text']
        if 'rating' in data:
            review['rating'] = data['rating']
        review['updated_at'] = datetime.now().isoformat()
        data_manager.update(Review(**review))
        return review, 200

    @ns.doc('delete_review')
    @ns.response(204, 'Review deleted')
    def delete(self, review_id):
        """Delete a review given its ID"""
        if not data_manager.get(review_id, 'review'):
            api.abort(404, f"Review {review_id} not found")
        data_manager.delete(review_id, 'review')
        return '', 204

# Endpoints para User
@ns.route('/users')
class UserList(Resource):
    @ns.doc('create_user')
    @ns.expect(user_model)
    @ns.marshal_with(user_model, code=201)
    def post(self):
        """Create a new user"""
        data = request.json
        new_user = User(**data)
        data_manager.save(new_user)
        return new_user, 201

    @ns.doc('list_users')
    @ns.marshal_list_with(user_model)
    def get(self):
        """List all users"""
        users = data_manager.get_all('user')
        return users, 200

@ns.route('/users/<string:user_id>')
@ns.param('user_id', 'The user identifier')
class UserResource(Resource):
    @ns.doc('get_user')
    @ns.marshal_with(user_model)
    def get(self, user_id):
        """Fetch a user given its ID"""
        user = data_manager.get(user_id, 'user')
        if not user:
            api.abort(404, f"User {user_id} not found")
        return user, 200

    @ns.doc('update_user')
    @ns.expect(user_model)
    @ns.marshal_with(user_model)
    def put(self, user_id):
        """Update a user given its ID"""
        data = request.json
        user = data_manager.get(user_id, 'user')
        if not user:
            api.abort(404, f"User {user_id} not found")
        if 'email' in data:
            user['email'] = data['email']
        if 'password' in data:
            user['password'] = data['password']
        if 'first_name' in data:
            user['first_name'] = data['first_name']
        if 'last_name' in data:
            user['last_name'] = data['last_name']
        user['updated_at'] = datetime.now().isoformat()
        data_manager.update(User(**user))
        return user, 200

    @ns.doc('delete_user')
    @ns.response(204, 'User deleted')
    def delete(self, user_id):
        """Delete a user given its ID"""
        if not data_manager.get(user_id, 'user'):
            api.abort(404, f"User {user_id} not found")
        data_manager.delete(user_id, 'user')
        return '', 204

if __name__ == '__main__':
    app.run(debug=True)
