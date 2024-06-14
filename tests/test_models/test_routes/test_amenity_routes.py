import unittest
import json
from app import app
from models import data_manager
from models.amenity import Amenity

class TestAmenityRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        # Clear amenities before each test
        data_manager.storage['Amenity'] = {}

    def test_create_amenity(self):
        response = self.app.post('/amenities', data=json.dumps({
            'name': 'WiFi'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['name'], 'WiFi')

    def test_create_amenity_missing_fields(self):
        response = self.app.post('/amenities', data=json.dumps({}), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_create_duplicate_amenity(self):
        amenity = Amenity(name='WiFi')
        data_manager.save(amenity)
        response = self.app.post('/amenities', data=json.dumps({
            'name': 'WiFi'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 409)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_get_amenities(self):
        amenity1 = Amenity(name='WiFi')
        amenity2 = Amenity(name='Pool')
        data_manager.save(amenity1)
        data_manager.save(amenity2)

        response = self.app.get('/amenities')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)

    def test_get_amenity(self):
        amenity = Amenity(name='WiFi')
        data_manager.save(amenity)
        response = self.app.get(f'/amenities/{amenity.id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'WiFi')

    def test_update_amenity(self):
        amenity = Amenity(name='WiFi')
        data_manager.save(amenity)
        response = self.app.put(f'/amenities/{amenity.id}', data=json.dumps({
            'name': 'High-Speed WiFi'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'High-Speed WiFi')

    def test_delete_amenity(self):
        amenity = Amenity(name='WiFi')
        data_manager.save(amenity)
        response = self.app.delete(f'/amenities/{amenity.id}')
        self.assertEqual(response.status_code, 204)
        self.assertIsNone(data_manager.get(amenity.id, 'Amenity'))

if __name__ == '__main__':
    unittest.main()