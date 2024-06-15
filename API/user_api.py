from flask import request
from flask_restx import Namespace, Resource, fields
from data_manager import DataManager
import uuid
from datetime import datetime

ns = Namespace('users', description='Operations related to users')
data_manager = DataManager()

# Model definition for a User
user_model = ns.model('User', {
    'id': fields.String(required=True, description='The user ID'),
    'username': fields.String(required=True, description='Username'),
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='Password'),
    'created_at': fields.DateTime(required=True, description='Date and time user was created'),
    'updated_at': fields.DateTime(required=True, description='Date and time user was last updated')
})


@ns.route('/')
class Users(Resource):
    @ns.marshal_list_with(user_model)
    def get(self): # Obtener todos los user.
        return data_manager.get_all_users()

    @ns.expect(user_model)
    @ns.response(201, 'User created')
    @ns.response(400, 'Invalid request')
    def post(self): # Crear user.
        new_user_data = request.json
        new_user_data['id'] = str(uuid.uuid4())
        new_user_data['created_at'] = datetime.now()
        new_user_data['updated_at'] = datetime.now()
        user_id = data_manager.save_user(new_user_data)
        return {
            'message': 'User created',
            'user_id': user_id
        }, 201


@ns.route('/<string:user_id>')
class UserResource(Resource):
    @ns.marshal_with(user_model)
    @ns.response(404, 'User not found')
    def get(self, user_id): #Optener user por su ID.
        user_data = data_manager.get_user(user_id)
        if user_data:
            return user_data
        else:
            ns.abort(404, "User not found")

    @ns.response(204, 'User deleted')
    @ns.response(404, 'User not found')
    def delete(self, user_id): # Eliminar user.
        if data_manager.delete_user(user_id):
            return '', 204
        else:
            ns.abort(404, "User not found")

    @ns.expect(user_model)
    @ns.response(204, 'User updated')
    @ns.response(400, 'Invalid request')
    @ns.response(404, 'User not found')
    def put(self, user_id): # Actualizar users.
        new_user_data = request.json
        new_user_data['id'] = user_id
        new_user_data['updated_at'] = datetime.now()
        if data_manager.update_user(user_id, new_user_data):
            return '', 204
        else:
            ns.abort(404, "User not found")