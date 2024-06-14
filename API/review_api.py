from flask_restx import Namespace, Resource, fields
from model.review import Review
from persistence.data_manager import DataManager

ns = Namespace('reviews', description='Operations related to reviews')

review_model = ns.model('Review', {
    'user': fields.String(required=True, description='The user email'),
    'place': fields.String(required=True, description='The place name'),
    'text': fields.String(required=True, description='The review text'),
    'rating': fields.Integer(required=True, description='The review rating')
})

data_manager = DataManager()

@ns.route('/')
class ReviewList(Resource):
    @ns.doc('create_review')
    @ns.expect(review_model)
    @ns.marshal_with(review_model, code=201)
    def post(self):
        """Create a new review"""
        data = ns.payload
        new_review = Review(**data)
        data_manager.save(new_review)
        return new_review, 201

    @ns.doc('list_reviews')
    @ns.marshal_list_with(review_model)
    def get(self):
        """List all reviews"""
        reviews = data_manager.get_all('review')
        return reviews, 200

@ns.route('/<string:review_id>')
@ns.param('review_id', 'The review identifier')
class ReviewResource(Resource):
    @ns.doc('get_review')
    @ns.marshal_with(review_model)
    def get(self, review_id):
        """Fetch a review given its ID"""
        review = data_manager.get(review_id, 'review')
        if not review:
            ns.abort(404, f"Review {review_id} not found")
        return review, 200

    @ns.doc('update_review')
    @ns.expect(review_model)
    @ns.marshal_with(review_model)
    def put(self, review_id):
        """Update a review given its ID"""
        data = ns.payload
        review = data_manager.get(review_id, 'review')
        if not review:
            ns.abort(404, f"Review {review_id} not found")
        for key, value in data.items():
            setattr(review, key, value)
        review.updated_at = datetime.now()
        data_manager.update(review)
        return review, 200

    @ns.doc('delete_review')
    @ns.response(204, 'Review deleted')
    def delete(self, review_id):
        """Delete a review given its ID"""
        if not data_manager.get(review_id, 'review'):
            ns.abort(404, f"Review {review_id} not found")
        data_manager.delete(review_id, 'review')
        return '', 204
