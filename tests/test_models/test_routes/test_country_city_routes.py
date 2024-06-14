import unittest
import json
from app import app
from models import data_manager
from models.city import City

class TestCountryCityRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        # Clear cities before each test
        data_manager.storage['City'] = {}

    def test_get_countries(self):
        response = self.app.get('/countries')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertGreaterEqual(len(data), 1)

    def test_get_country(self):
        response = self.app.get('/countries/US')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['code'], 'US')

    def test_get_country_not_found(self):
        response = self.app.get('/countries/XX')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_create_city(self):
        response = self.app.post('/cities', data=json.dumps({
            'name': 'New York',
            'country_code': 'US'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'New York')

    def test_create_city_invalid_country(self):
        response = self.app.post('/cities', data=json.dumps({
            'name': 'Invalid City',
            'country_code': 'XX'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_get_cities(self):
        city1 = City(name='New York', country_code='US')
        city2 = City(name='Los Angeles', country_code='US')
        data_manager.save(city1)
        data_manager.save(city2)

        response = self.app.get('/cities')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)

    def test_get_city(self):
        city = City(name='New York', country_code='US')
        data_manager.save(city)
        response = self.app.get(f'/cities/{city.id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'New York')

    def test_update_city(self):
        city = City(name='New York', country_code='US')
        data_manager.save(city)
        response = self.app.put(f'/cities/{city.id}', data=json.dumps({
            'name': 'NYC'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'NYC')

    def test_delete_city(self):
        city = City(name='New York', country_code='US')
        data_manager.save(city)
        response = self.app.delete(f'/cities/{city.id}')
        self.assertEqual(response.status_code, 204)
        self.assertIsNone(data_manager.get(city.id, 'City'))

if __name__ == '__main__':
    unittest.main()