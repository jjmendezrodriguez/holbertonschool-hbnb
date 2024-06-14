from flask_restx import Namespace, Resource, fields
from model.city import City
from persistence.data_manager import DataManager

ns = Namespace('cities', description='Operations related to cities')

city_model = ns.model('City', {
    'name': fields.String(required=True, description='The city name'),
    'country_code': fields.String(required=True, description='The ISO country code')
})

data_manager = DataManager()

@ns.route('/')
class CityList(Resource):
    @ns.doc('create_city')
    @ns.expect(city_model)
    @ns.marshal_with(city_model, code=201)
    def post(self):
        """Create a new city"""
        data = ns.payload
        new_city = City(**data)
        data_manager.save(new_city)
        return new_city, 201

    @ns.doc('list_cities')
    @ns.marshal_list_with(city_model)
    def get(self):
        """List all cities"""
        cities = data_manager.get_all('city')
        return cities, 200

@ns.route('/<string:city_id>')
@ns.param('city_id', 'The city identifier')
class CityResource(Resource):
    @ns.doc('get_city')
    @ns.marshal_with(city_model)
    def get(self, city_id):
        """Fetch a city given its ID"""
        city = data_manager.get(city_id, 'city')
        if not city:
            ns.abort(404, f"City {city_id} not found")
        return city, 200

    @ns.doc('update_city')
    @ns.expect(city_model)
    @ns.marshal_with(city_model)
    def put(self, city_id):
        """Update a city given its ID"""
        data = ns.payload
        city = data_manager.get(city_id, 'city')
        if not city:
            ns.abort(404, f"City {city_id} not found")
        for key, value in data.items():
            setattr(city, key, value)
        city.updated_at = datetime.now()
        data_manager.update(city)
        return city, 200

    @ns.doc('delete_city')
    @ns.response(204, 'City deleted')
    def delete(self, city_id):
        """Delete a city given its ID"""
        if not data_manager.get(city_id, 'city'):
            ns.abort(404, f"City {city_id} not found")
        data_manager.delete(city_id, 'city')
        return '', 204
