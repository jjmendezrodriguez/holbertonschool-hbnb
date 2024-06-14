from flask_restx import Namespace, Resource, fields
from model.place import Place
from data_manager import DataManager

ns = Namespace('places', description='Operations related to places')

place_model = ns.model('Place', {
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

data_manager = DataManager()

@ns.route('/')
class PlaceList(Resource):
    @ns.doc('create_place')
    @ns.expect(place_model)
    @ns.marshal_with(place_model, code=201)
    def post(self):
        """Create a new place"""
        data = ns.payload
        new_place = Place(**data)
        data_manager.save(new_place)
        return new_place, 201

    @ns.doc('list_places')
    @ns.marshal_list_with(place_model)
    def get(self):
        """List all places"""
        places = data_manager.get_all('place')
        return places, 200

@ns.route('/<string:place_id>')
@ns.param('place_id', 'The place identifier')
class PlaceResource(Resource):
    @ns.doc('get_place')
    @ns.marshal_with(place_model)
    def get(self, place_id):
        """Fetch a place given its ID"""
        place = data_manager.get(place_id, 'place')
        if not place:
            ns.abort(404, f"Place {place_id} not found")
        return place, 200

    @ns.doc('update_place')
    @ns.expect(place_model)
    @ns.marshal_with(place_model)
    def put(self, place_id):
        """Update a place given its ID"""
        data = ns.payload
        place = data_manager.get(place_id, 'place')
        if not place:
            ns.abort(404, f"Place {place_id} not found")
        for key, value in data.items():
            setattr(place, key, value)
        place.updated_at = datetime.now()
        data_manager.update(place)
        return place, 200

    @ns.doc('delete_place')
    @ns.response(204, 'Place deleted')
    def delete(self, place_id):
        """Delete a place given its ID"""
        if not data_manager.get(place_id, 'place'):
            ns.abort(404, f"Place {place_id} not found")
        data_manager.delete(place_id, 'place')
        return '', 204
