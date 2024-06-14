from flask_restx import Namespace, Resource, fields
from model.user import User
from persistence.data_manager import DataManager

ns = Namespace('users', description='Operations related to users')

user_model = ns.model('User', {
    'email': fields.String(required=True, description='The user email'),
    'password': fields.String(required=True, description='The user password'),
    'first_name': fields.String(required=True, description='The user first name'),
    'last_name': fields.String(required=True, description='The user last name')
})

data_manager = DataManager()

@ns.route('/')
class UserList(Resource):
    @ns.doc('create_user')
    @ns.expect(user_model)
    @ns.marshal_with(user_model, code=201)
    def post(self):
        """Create a new user"""
        data = ns.payload
        new_user = User(**data)
        data_manager.save(new_user)
        return new_user, 201

    @ns.doc('list_users')
    @ns.marshal_list_with(user_model)
    def get(self):
        """List all users"""
        users = data_manager.get_all('user')
        return users, 200

@ns.route('/<string:user_id>')
@ns.param('user_id', 'The user identifier')
class UserResource(Resource):
    @ns.doc('get_user')
    @ns.marshal_with(user_model)
    def get(self, user_id):
        """Fetch a user given its ID"""
        user = data_manager.get(user_id, 'user')
        if not user:
            ns.abort(404, f"User {user_id} not found")
        return user, 200

    @ns.doc('update_user')
    @ns.expect(user_model)
    @ns.marshal_with(user_model)
    def put(self, user_id):
        """Update a user given its ID"""
        data = ns.payload
        user = data_manager.get(user_id, 'user')
        if not user:
            ns.abort(404, f"User {user_id} not found")
        for key, value in data.items():
            setattr(user, key, value)
        user.updated_at = datetime.now()
        data_manager.update(user)
        return user, 200

    @ns.doc('delete_user')
    @ns.response(204, 'User deleted')
    def delete(self, user_id):
        """Delete a user given its ID"""
        if not data_manager.get(user_id, 'user'):
            ns.abort(404, f"User {user_id} not found")
        data_manager.delete(user_id, 'user')
        return '', 204
