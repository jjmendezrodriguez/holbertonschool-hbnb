from flask import request
from flask_restx import Namespace, Resource, fields
from datetime import datetime
import uuid
from data_manager import DataManager

# Definición del namespace para las amenities
ns = Namespace('amenities', description='Operations related to amenities')
data_manager = DataManager()

# Definición del modelo para una Amenity
amenity_model = ns.model('Amenity', {
    'id': fields.String(required=True, description='ID of Amenity'),
    'name': fields.String(required=True, description='The amenity name'),
    'created_at': fields.DateTime(required=True, description='Date and time amenity was created'),
    'updated_at': fields.DateTime(required=True, description='Date and time when the amenity was last updated')
})

# Ruta para gestionar la colección de amenities
@ns.route('/')
class Amenities(Resource):
    @ns.marshal_list_with(amenity_model)
    def get(self): # Obtener todas las amenities.
        return data_manager.get_all('amenity'), 200

    @ns.expect(amenity_model)
    @ns.response(201, 'Amenity created')
    @ns.response(400, 'Invalid request')
    def post(self): # Crear una nueva amenity.
        new_amenity_data = request.json
        new_amenity_data['id'] = str(uuid.uuid4())
        new_amenity_data['created_at'] = datetime.now()
        new_amenity_data['updated_at'] = datetime.now()
        data_manager.save(new_amenity_data)
        return {
            'message': 'Amenity created',
            'amenity_id': new_amenity_data['id']
        }, 201

# Ruta para gestionar una amenity específica por su ID
@ns.route('/<string:amenity_id>')
class AmenityList(Resource):
    @ns.marshal_with(amenity_model)
    @ns.response(404, 'Amenity not found')
    def get(self, amenity_id): # Obtener una amenity por su ID.
        amenity_data = data_manager.get(amenity_id, 'amenity')
        if amenity_data:
            return amenity_data, 200
        else:
            ns.abort(404, "Amenity not found")

    @ns.response(204, 'Amenity deleted')
    @ns.response(404, 'Amenity not found')
    def delete(self, amenity_id): # Eliminar una amenity existente.
        if data_manager.delete(amenity_id, 'amenity'):
            return '', 204
        else:
            ns.abort(404, "Amenity not found")

    @ns.expect(amenity_model)
    @ns.response(204, 'Amenity updated')
    @ns.response(400, 'Invalid request')
    @ns.response(404, 'Amenity not found')
    def put(self, amenity_id): # Actualizar una amenity existente.
        new_amenity_data = request.json
        new_amenity_data['id'] = amenity_id
        new_amenity_data['updated_at'] = datetime.now()
        if data_manager.update(amenity_id, new_amenity_data):
            return '', 204
        else:
            ns.abort(404, "Amenity not found")