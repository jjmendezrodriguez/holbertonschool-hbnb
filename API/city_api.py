from flask import request
from flask_restx import Namespace, Resource, fields
from data_manager import DataManager
import uuid
from datetime import datetime

ns = Namespace('cities', description='Operations related to cities')
data_manager = DataManager()


city_model = ns.model('City', {
    'id': fields.String(required=True, description='The city ID'),
    'name': fields.String(required=True, description='The city name'),
    'country_id': fields.Integer(required=True, description='Country ID'),
    'created_at': fields.DateTime(required=True, description='Date and time when city was created'),
    'updated_at': fields.DateTime(required=True, description='Date and time city was last updated')
})


@ns.route('/')
class Cities(Resource):
    @ns.marshal_list_with(city_model)
    def get(self): # Crea una nueva ciudad.
        return data_manager.get_all_cities()

    @ns.expect(city_model)
    @ns.response(201, 'City created')
    @ns.response(400, 'Invalid request')
    def post(self): # Lista de todas las ciudades.
        new_city_data = request.json
        new_city_data['id'] = str(uuid.uuid4())
        new_city_data['created_at'] = datetime.now()
        new_city_data['updated_at'] = datetime.now()
        city_id = data_manager.save_city(new_city_data)
        return {
            'message': 'City created',
            'city_id': city_id
        }, 201


@ns.route('/<string:city_id>')
class CityList(Resource):
    @ns.marshal_with(city_model)
    @ns.response(404, 'City not found')
    def get(self, city_id): # Obtiene una ciudad por su ID.
        city_data = data_manager.get_city(city_id)
        if city_data:
            return city_data
        else:
            ns.abort(404, "City not found")

    @ns.response(204, 'City deleted')
    @ns.response(404, 'City not found')
    def delete(self, city_id): # Elimina la ciudad.
        if data_manager.delete_city(city_id):
            return '', 204
        else:
            ns.abort(404, "City not found")

    @ns.expect(city_model)
    @ns.response(204, 'City updated')
    @ns.response(400, 'Invalid request')
    @ns.response(404, 'City not found')
    def put(self, city_id): # Actualiza una ciudad existente.
        new_city_data = request.json
        new_city_data['id'] = city_id
        new_city_data['updated_at'] = datetime.now()
        if data_manager.update_city(city_id, new_city_data):
            return '', 204
        else:
            ns.abort(404, "City not found")