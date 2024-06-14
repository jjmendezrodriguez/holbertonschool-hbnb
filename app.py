from flask import Flask, request, jsonify
from models import data_manager
from models.user import User
from models.country import Country
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import json

app = Flask(__name__)

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if 'email' not in data or 'first_name' not in data or 'last_name' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        user = User(email=data['email'], first_name=data['first_name'], last_name=data['last_name'])
        data_manager.save(user)
        return jsonify({
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'created_at': user.created_at,
            'updated_at': user.updated_at
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 409

@app.route('/users', methods=['GET'])
def get_users():
    users = data_manager.storage['User'].values()
    return jsonify([{
        'id': user.id,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'created_at': user.created_at,
        'updated_at': user.updated_at
    } for user in users]), 200

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = data_manager.get(user_id, 'User')
    if user:
        return jsonify({
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'created_at': user.created_at,
            'updated_at': user.updated_at
        }), 200
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user = data_manager.get(user_id, 'User')
    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()
    if 'first_name' in data:
        user.first_name = data['first_name']
    if 'last_name' in data:
        user.last_name = data['last_name']

    user.save()
    data_manager.update(user)
    return jsonify({
        'id': user.id,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'created_at': user.created_at,
        'updated_at': user.updated_at
    }), 200

@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = data_manager.get(user_id, 'User')
    if not user:
        return jsonify({'error': 'User not found'}), 404

    data_manager.delete(user_id, 'User')
    return '', 204

# Load Country data
with open('data/countries.json', 'r') as f:
    countries = json.load(f)
    for country_data in countries:
        country = Country(code=country_data['code'], name=country_data['name'])
        data_manager.save(country)

@app.route('/countries', methods=['GET'])
def get_countries():
    countries = data_manager.storage['Country'].values()
    return jsonify([{
        'code': country.code,
        'name': country.name
    } for country in countries]), 200

@app.route('/countries/<country_code>', methods=['GET'])
def get_country(country_code):
    country = data_manager.get(country_code, 'Country')
    if country:
        return jsonify({
            'code': country.code,
            'name': country.name
        }), 200
    else:
        return jsonify({'error': 'Country not found'}), 404

@app.route('/countries/<country_code}/cities', methods=['GET'])
def get_cities_by_country(country_code):
    country = data_manager.get(country_code, 'Country')
    if not country:
        return jsonify({'error': 'Country not found'}), 404

    cities = [city for city in data_manager.storage['City'].values() if city.country_code == country_code]
    return jsonify([{
        'id': city.id,
        'name': city.name,
        'country_code': city.country_code,
        'created_at': city.created_at,
        'updated_at': city.updated_at
    } for city in cities]), 200

@app.route('/cities', methods=['POST'])
def create_city():
    data = request.get_json()
    if 'name' not in data or 'country_code' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    country = data_manager.get(data['country_code'], 'Country')
    if not country:
        return jsonify({'error': 'Invalid country code'}), 400

    city = City(name=data['name'], country_code=data['country_code'])
    data_manager.save(city)
    return jsonify({
        'id': city.id,
        'name': city.name,
        'country_code': city.country_code,
        'created_at': city.created_at,
        'updated_at': city.updated_at
    }), 201

@app.route('/cities', methods=['GET'])
def get_cities():
    cities = data_manager.storage['City'].values()
    return jsonify([{
        'id': city.id,
        'name': city.name,
        'country_code': city.country_code,
        'created_at': city.created_at,
        'updated_at': city.updated_at
    } for city in cities]), 200

@app.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    city = data_manager.get(city_id, 'City')
    if city:
        return jsonify({
            'id': city.id,
            'name': city.name,
            'country_code': city.country_code,
            'created_at': city.created_at,
            'updated_at': city.updated_at
        }), 200
    else:
        return jsonify({'error': 'City not found'}), 404

@app.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    city = data_manager.get(city_id, 'City')
    if not city:
        return jsonify({'error': 'City not found'}), 404

    data = request.get_json()
    if 'name' in data:
        city.name = data['name']
    city.save()
    data_manager.update(city)
    return jsonify({
        'id': city.id,
        'name': city.name,
        'country_code': city.country_code,
        'created_at': city.created_at,
        'updated_at': city.updated_at
    }), 200

@app.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    city = data_manager.get(city_id, 'City')
    if not city:
        return jsonify({'error': 'City not found'}), 404

    data_manager.delete(city_id, 'City')
    return '', 204

@app.route('/amenities', methods=['POST'])
def create_amenity():
    data = request.get_json()
    if 'name' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    if any(amenity.name == data['name'] for amenity in data_manager.storage['Amenity'].values()):
        return jsonify({'error': 'Amenity already exists'}), 409

    amenity = Amenity(name=data['name'])
    data_manager.save(amenity)
    return jsonify({
        'id': amenity.id,
        'name': amenity.name,
        'created_at': amenity.created_at,
        'updated_at': amenity.updated_at
    }), 201

@app.route('/amenities', methods=['GET'])
def get_amenities():
    amenities = data_manager.storage['Amenity'].values()
    return jsonify([{
        'id': amenity.id,
        'name': amenity.name,
        'created_at': amenity.created_at,
        'updated_at': amenity.updated_at
    } for amenity in amenities]), 200

@app.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    amenity = data_manager.get(amenity_id, 'Amenity')
    if amenity:
        return jsonify({
            'id': amenity.id,
            'name': amenity.name,
            'created_at': amenity.created_at,
            'updated_at': amenity.updated_at
        }), 200
    else:
        return jsonify({'error': 'Amenity not found'}), 404

@app.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    amenity = data_manager.get(amenity_id, 'Amenity')
    if not amenity:
        return jsonify({'error': 'Amenity not found'}), 404

    data = request.get_json()
    if 'name' in data:
        if any(a.name == data['name'] and a.id != amenity_id for a in data_manager.storage['Amenity'].values()):
            return jsonify({'error': 'Amenity name already exists'}), 409
        amenity.name = data['name']
    amenity.save()
    data_manager.update(amenity)
    return jsonify({
        'id': amenity.id,
        'name': amenity.name,
        'created_at': amenity.created_at,
        'updated_at': amenity.updated_at
    }), 200

@app.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    amenity = data_manager.get(amenity_id, 'Amenity')
    if not amenity:
        return jsonify({'error': 'Amenity not found'}), 404

    data_manager.delete(amenity_id, 'Amenity')
    return '', 204

@app.route('/places', methods=['POST'])
def create_place():
    data = request.get_json()
    required_fields = ['name', 'description', 'address', 'city_id', 'latitude', 'longitude', 'host_id', 'number_of_rooms', 'number_of_bathrooms', 'price_per_night', 'max_guests', 'amenity_ids']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    city = data_manager.get(data['city_id'], 'City')
    if not city:
        return jsonify({'error': 'Invalid city_id'}), 400

    place = Place(name=data['name'], description=data['description'], address=data['address'], city_id=data['city_id'], latitude=data['latitude'], longitude=data['longitude'], host_id=data['host_id'], number_of_rooms=data['number_of_rooms'], number_of_bathrooms=data['number_of_bathrooms'], price_per_night=data['price_per_night'], max_guests=data['max_guests'])
    for amenity_id in data['amenity_ids']:
        amenity = data_manager.get(amenity_id, 'Amenity')
        if amenity:
            place.add_amenity(amenity)
        else:
            return jsonify({'error': f'Invalid amenity_id: {amenity_id}'}), 400

    data_manager.save(place)
    return jsonify({
        'id': place.id,
        'name': place.name,
        'description': place.description,
        'address': place.address,
        'city_id': place.city_id,
        'latitude': place.latitude,
        'longitude': place.longitude,
        'host_id': place.host_id,
        'number_of_rooms': place.number_of_rooms,
        'number_of_bathrooms': place.number_of_bathrooms,
        'price_per_night': place.price_per_night,
        'max_guests': place.max_guests,
        'amenity_ids': [amenity.id for amenity in place.amenities],
        'created_at': place.created_at,
        'updated_at': place.updated_at
    }), 201

@app.route('/places', methods=['GET'])
def get_places():
    places = data_manager.storage['Place'].values()
    return jsonify([{
        'id': place.id,
        'name': place.name,
        'description': place.description,
        'address': place.address,
        'city_id': place.city_id,
        'latitude': place.latitude,
        'longitude': place.longitude,
        'host_id': place.host_id,
        'number_of_rooms': place.number_of_rooms,
        'number_of_bathrooms': place.number_of_bathrooms,
        'price_per_night': place.price_per_night,
        'max_guests': place.max_guests,
        'amenity_ids': [amenity.id for amenity in place.amenities],
        'created_at': place.created_at,
        'updated_at': place.updated_at
    } for place in places]), 200

@app.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    place = data_manager.get(place_id, 'Place')
    if place:
        return jsonify({
            'id': place.id,
            'name': place.name,
            'description': place.description,
            'address': place.address,
            'city_id': place.city_id,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'host_id': place.host_id,
            'number_of_rooms': place.number_of_rooms,
            'number_of_bathrooms': place.number_of_bathrooms,
            'price_per_night': place.price_per_night,
            'max_guests': place.max_guests,
            'amenity_ids': [amenity.id for amenity in place.amenities],
            'created_at': place.created_at,
            'updated_at': place.updated_at
        }), 200
    else:
        return jsonify({'error': 'Place not found'}), 404

@app.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    place = data_manager.get(place_id, 'Place')
    if not place:
        return jsonify({'error': 'Place not found'}), 404

    data = request.get_json()
    if 'name' in data:
        place.name = data['name']
    if 'description' in data:
        place.description = data['description']
    if 'address' in data:
        place.address = data['address']
    if 'latitude' in data:
        place.latitude = data['latitude']
    if 'longitude' in data:
        place.longitude = data['longitude']
    if 'number_of_rooms' in data:
        place.number_of_rooms = data['number_of_rooms']
    if 'number_of_bathrooms' in data:
        place.number_of_bathrooms = data['number_of_bathrooms']
    if 'price_per_night' in data:
        place.price_per_night = data['price_per_night']
    if 'max_guests' in data:
        place.max_guests = data['max_guests']
    if 'amenity_ids' in data:
        place.amenities = []
        for amenity_id in data['amenity_ids']:
            amenity = data_manager.get(amenity_id, 'Amenity')
            if amenity:
                place.add_amenity(amenity)
            else:
                return jsonify({'error': f'Invalid amenity_id: {amenity_id}'}), 400

    place.save()
    data_manager.update(place)
    return jsonify({
        'id': place.id,
        'name': place.name,
        'description': place.description,
        'address': place.address,
        'city_id': place.city_id,
        'latitude': place.latitude,
        'longitude': place.longitude,
        'host_id': place.host_id,
        'number_of_rooms': place.number_of_rooms,
        'number_of_bathrooms': place.number_of_bathrooms,
        'price_per_night': place.price_per_night,
        'max_guests': place.max_guests,
        'amenity_ids': [amenity.id for amenity in place.amenities],
        'created_at': place.created_at,
        'updated_at': place.updated_at
    }), 200

@app.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    place = data_manager.get(place_id, 'Place')
    if not place:
        return jsonify({'error': 'Place not found'}), 404

    data_manager.delete(place_id, 'Place')
    return '', 204

@app.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    place = data_manager.get(place_id, 'Place')
    if not place:
        return jsonify({'error': 'Place not found'}), 404

    data = request.get_json()
    if 'user_id' not in data or 'rating' not in data or 'comment' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    user = data_manager.get(data['user_id'], 'User')
    if not user:
        return jsonify({'error': 'Invalid user_id'}), 400

    if not (1 <= data['rating'] <= 5):
        return jsonify({'error': 'Rating must be between 1 and 5'}), 400

    review = Review(user_id=data['user_id'], place_id=place_id, rating=data['rating'], comment=data['comment'])
    data_manager.save(review)
    return jsonify({
        'id': review.id,
        'user_id': review.user_id,
        'place_id': review.place_id,
        'rating': review.rating,
        'comment': review.comment,
        'created_at': review.created_at,
        'updated_at': review.updated_at
    }), 201

@app.route('/users/<user_id>/reviews', methods=['GET'])
def get_reviews_by_user(user_id):
    user = data_manager.get(user_id, 'User')
    if not user:
        return jsonify({'error': 'User not found'}), 404

    reviews = [review for review in data_manager.storage['Review'].values() if review.user_id == user_id]
    return jsonify([{
        'id': review.id,
        'user_id': review.user_id,
        'place_id': review.place_id,
        'rating': review.rating,
        'comment': review.comment,
        'created_at': review.created_at,
        'updated_at': review.updated_at
    } for review in reviews]), 200

@app.route('/places/<place_id>/reviews', methods=['GET'])
def get_reviews_by_place(place_id):
    place = data_manager.get(place_id, 'Place')
    if not place:
        return jsonify({'error': 'Place not found'}), 404

    reviews = [review for review in data_manager.storage['Review'].values() if review.place_id == place_id]
    return jsonify([{
        'id': review.id,
        'user_id': review.user_id,
        'place_id': review.place_id,
        'rating': review.rating,
        'comment': review.comment,
        'created_at': review.created_at,
        'updated_at': review.updated_at
    } for review in reviews]), 200

@app.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    review = data_manager.get(review_id, 'Review')
    if review:
        return jsonify({
            'id': review.id,
            'user_id': review.user_id,
            'place_id': review.place_id,
            'rating': review.rating,
            'comment': review.comment,
            'created_at': review.created_at,
            'updated_at': review.updated_at
        }), 200
    else:
        return jsonify({'error': 'Review not found'}), 404

@app.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    review = data_manager.get(review_id, 'Review')
    if not review:
        return jsonify({'error': 'Review not found'}), 404

    data = request.get_json()
    if 'rating' in data:
        if not (1 <= data['rating'] <= 5):
            return jsonify({'error': 'Rating must be between 1 and 5'}), 400
        review.rating = data['rating']
    if 'comment' in data:
        review.comment = data['comment']

    review.save()
    data_manager.update(review)
    return jsonify({
        'id': review.id,
        'user_id': review.user_id,
        'place_id': review.place_id,
        'rating': review.rating,
        'comment': review.comment,
        'created_at': review.created_at,
        'updated_at': review.updated_at
    }), 200

@app.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    review = data_manager.get(review_id, 'Review')
    if not review:
        return jsonify({'error': 'Review not found'}), 404

    data_manager.delete(review_id, 'Review')
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)

import unittest
import json
from app import app
from models import data_manager
from models.place import Place
from models.city import City
from models.amenity import Amenity

class TestPlaceRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        # Clear places, cities, and amenities before each test
        data_manager.storage['Place'] = {}
        data_manager.storage['City'] = {}
        data_manager.storage['Amenity'] = {}

        # Create a city and amenities for testing
        self.city = City(name='Test City', country_code='US')
        data_manager.save(self.city)
        self.amenity1 = Amenity(name='WiFi')
        self.amenity2 = Amenity(name='Pool')
        data_manager.save(self.amenity1)
        data_manager.save(self.amenity2)

    def test_create_place(self):
        response = self.app.post('/places', data=json.dumps({
            'name': 'Test Place',
            'description': 'A nice place',
            'address': '123 Main St',
            'city_id': self.city.id,
            'latitude': 45.0,
            'longitude': -75.0,
            'host_id': 'host123',
            'number_of_rooms': 2,
            'number_of_bathrooms': 1,
            'price_per_night': 100,
            'max_guests': 4,
            'amenity_ids': [self.amenity1.id, self.amenity2.id]
        }), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Test Place')

    def test_create_place_missing_fields(self):
        response = self.app.post('/places', data=json.dumps({
            'name': 'Test Place'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_get_places(self):
        place1 = Place(name='Place 1', description='A nice place', address='123 Main St', city_id=self.city.id, latitude=45.0, longitude=-75.0, host_id='host1', number_of_rooms=2, number_of_bathrooms=1, price_per_night=100, max_guests=4)
        place2 = Place(name='Place 2', description='Another nice place', address='456 Main St', city_id=self.city.id, latitude=46.0, longitude=-76.0, host_id='host2', number_of_rooms=3, number_of_bathrooms=2, price_per_night=150, max_guests=5)
        data_manager.save(place1)
        data_manager.save(place2)

        response = self.app.get('/places')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)

    def test_get_place(self):
        place = Place(name='Place 1', description='A nice place', address='123 Main St', city_id=self.city.id, latitude=45.0, longitude=-75.0, host_id='host1', number_of_rooms=2, number_of_bathrooms=1, price_per_night=100, max_guests=4)
        data_manager.save(place)
        response = self.app.get(f'/places/{place.id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Place 1')

    def test_update_place(self):
        place = Place(name='Place 1', description='A nice place', address='123 Main St', city_id=self.city.id, latitude=45.0, longitude=-75.0, host_id='host1', number_of_rooms=2, number_of_bathrooms=1, price_per_night=100, max_guests=4)
        data_manager.save(place)
        response = self.app.put(f'/places/{place.id}', data=json.dumps({
            'name': 'Updated Place',
            'price_per_night': 200
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Updated Place')
        self.assertEqual(data['price_per_night'], 200)

    def test_delete_place(self):
        place = Place(name='Place 1', description='A nice place', address='123 Main St', city_id=self.city.id, latitude=45.0, longitude=-75.0, host_id='host1', number_of_rooms=2, number_of_bathrooms=1, price_per_night=100, max_guests=4)
        data_manager.save(place)
        response = self.app.delete(f'/places/{place.id}')
        self.assertEqual(response.status_code, 204)
        self.assertIsNone(data_manager.get(place.id, 'Place'))

if __name__ == '__main__':
    app.run(debug=True)