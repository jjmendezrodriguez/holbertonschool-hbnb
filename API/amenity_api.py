from flask_restx import Namespace, Resource, fields
from model.amenity import Amenity
from persistence.data_manager import DataManager

ns = Namespace('amenities', description='Operations related to amenities')

amenity_model = ns.model('Amenity', {
    'name': fields.String(required=True, description='The amenity name'),
    'description': fields.String(required=True, description='The amenity description')
})

data_manager = DataManager()

@ns.route('/')
class AmenityList(Resource):
    @ns.doc('create_amenity')
    @ns.expect(amenity_model)
    @ns.marshal_with(amenity_model, code=201)
    def post(self):
        """Create a new amenity"""
        data = ns.payload
        new_amenity = Amenity(**data)
        data_manager.save(new_amenity)
        return new_amenity, 201

    @ns.doc('list_amenities')
    @ns.marshal_list_with(amenity_model)
    def get(self):
        """List all amenities"""
        amenities = data_manager.get_all('amenity')
        return amenities, 200

@ns.route('/<string:amenity_id>')
@ns.param('amenity_id', 'The amenity identifier')
class AmenityResource(Resource):
    @ns.doc('get_amenity')
    @ns.marshal_with(amenity_model)
    def get(self, amenity_id):
        """Fetch an amenity given its ID"""
        amenity = data_manager.get(amenity_id, 'amenity')
        if not amenity:
            ns.abort(404, f"Amenity {amenity_id} not found")
        return amenity, 200

    @ns.doc('update_amenity')
    @ns.expect(amenity_model)
    @ns.marshal_with(amenity_model)
    def put(self, amenity_id):
        """Update an amenity given its ID"""
        data = ns.payload
        amenity = data_manager.get(amenity_id, 'amenity')
        if not amenity:
            ns.abort(404, f"Amenity {amenity_id} not found")
        for key, value in data.items():
            setattr(amenity, key, value)
        amenity.updated_at = datetime.now()
        data_manager.update(amenity)
        return amenity, 200

    @ns.doc('delete_amenity')
    @ns.response(204, 'Amenity deleted')
    def delete(self, amenity_id):
        """Delete an amenity given its ID"""
        if not data_manager.get(amenity_id, 'amenity'):
            ns.abort(404, f"Amenity {amenity_id} not found")
        data_manager.delete(amenity_id, 'amenity')
        return '', 204
