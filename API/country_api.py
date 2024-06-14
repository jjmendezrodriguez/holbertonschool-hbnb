from flask_restx import Namespace, Resource, fields
from model.country import Country
from data_manager import DataManager

ns = Namespace('countries', description='Operations related to countries')

country_model = ns.model('Country', {
    'name': fields.String(required=True, description='The country name'),
    'code': fields.String(required=True, description='The country code')
})

data_manager = DataManager()

@ns.route('/')
class CountryList(Resource):
    @ns.doc('list_countries')
    @ns.marshal_list_with(country_model)
    def get(self):
        """List all countries"""
        countries = data_manager.get_all('country')
        return countries, 200

@ns.route('/<string:country_code>')
@ns.param('country_code', 'The country identifier')
class CountryResource(Resource):
    @ns.doc('get_country')
    @ns.marshal_with(country_model)
    def get(self, country_code):
        """Fetch a country given its code"""
        country = data_manager.get(country_code, 'country')
        if not country:
            ns.abort(404, f"Country {country_code} not found")
        return country, 200
