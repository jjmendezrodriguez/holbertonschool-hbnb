import unittest
import json
from app import app
from models.user import User
from models import data_manager

class TestUserRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        data_manager.storage['User'] = {}

    def test_create_user(self):
        response = self.app.post('/users', data=json.dumps({
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['email'], 'test@example.com')

    def test_create_user_missing_fields(self):
        response = self.app.post('/users', data=json.dumps({
            'email': 'test@example.com'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_get_users(self):
        user1 = User(email='user1@example.com', first_name='User1', last_name='One')
        user2 = User(email='user2@example.com', first_name='User2', last_name='Two')
        data_manager.save(user1)
        data_manager.save(user2)

        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)

    def test_get_user(self):
        user = User(email='user@example.com', first_name='User', last_name='Example')
        data_manager.save(user)
        response = self.app.get(f'/users/{user.id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['email'], 'user@example.com')

    def test_get_user_not_found(self):
        response = self.app.get('/users/nonexistent_id')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_update_user(self):
        user = User(email='user@example.com', first_name='User', last_name='Example')
        data_manager.save(user)
        response = self.app.put(f'/users/{user.id}', data=json.dumps({
            'first_name': 'UpdatedUser'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['first_name'], 'UpdatedUser')

    def test_delete_user(self):
        user = User(email='user@example.com', first_name='User', last_name='Example')
        data_manager.save(user)
        response = self.app.delete(f'/users/{user.id}')
        self.assertEqual(response.status_code, 204)
        self.assertIsNone(data_manager.get(user.id, 'User'))

if __name__ == '__main__':
    unittest.main()