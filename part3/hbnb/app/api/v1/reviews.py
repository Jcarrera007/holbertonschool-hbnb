"""
Review API endpoints for the HBnB application.

This module defines the RESTful API endpoints for review management.
"""

from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.models.review import Review
from app.api.v1.places import places_storage

# Create namespace for review endpoints
api = Namespace('reviews', description='Review operations')

# Define review model for Swagger documentation
review_model = api.model('Review', {
    'id': fields.String(readonly=True, description='The review unique identifier'),
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, description='Rating (1-5)'),
    'user_id': fields.String(required=True, description='Reviewer user ID'),
    'place_id': fields.String(required=True, description='Place ID'),
    'created_at': fields.String(readonly=True, description='Creation timestamp'),
    'updated_at': fields.String(readonly=True, description='Last update timestamp')
})

review_input_model = api.model('ReviewInput', {
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, description='Rating (1-5)', min=1, max=5),
    'place_id': fields.String(required=True, description='Place ID')
})

review_update_model = api.model('ReviewUpdate', {
    'text': fields.String(description='Review text'),
    'rating': fields.Integer(description='Rating (1-5)', min=1, max=5)
})

# In-memory storage for demonstration
reviews_storage = {}


def is_admin():
    """Check if the current user is an admin."""
    claims = get_jwt()
    return claims.get('is_admin', False)


def can_modify_review(review):
    """Check if current user can modify the review."""
    current_user_id = get_jwt_identity()
    
    # Admin can modify any review
    if is_admin():
        return True
    
    # User can modify their own review
    return review.user_id == current_user_id


def can_review_place(place_id):
    """Check if current user can review this place."""
    current_user_id = get_jwt_identity()
    place = places_storage.get(place_id)
    
    if not place:
        return False, "Place not found"
    
    # Users cannot review their own places
    if place.owner_id == current_user_id:
        return False, "You cannot review your own place"
    
    # Check if user already reviewed this place
    for review in reviews_storage.values():
        if review.user_id == current_user_id and review.place_id == place_id:
            return False, "You have already reviewed this place"
    
    return True, "OK"


@api.route('/')
class ReviewList(Resource):
    @api.doc('list_reviews')
    @api.marshal_list_with(review_model)
    def get(self):
        """Get all reviews (public endpoint)"""
        return list(reviews_storage.values())

    @api.doc('create_review')
    @api.expect(review_input_model)
    @api.marshal_with(review_model, code=201)
    @jwt_required()
    def post(self):
        """Create a new review (authenticated users only)"""
        try:
            data = request.get_json()
            current_user_id = get_jwt_identity()
            
            # Validate required fields
            required_fields = ['text', 'rating', 'place_id']
            for field in required_fields:
                if field not in data:
                    api.abort(400, f'{field} is required')
            
            # Check if user can review this place
            can_review, message = can_review_place(data['place_id'])
            if not can_review:
                api.abort(403, message)
            
            # Create new review
            review = Review(
                text=data['text'],
                rating=data['rating'],
                user_id=current_user_id,
                place_id=data['place_id']
            )
            
            # Store review
            reviews_storage[review.id] = review
            
            return review.to_dict(), 201
            
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, f'Internal server error: {str(e)}')


@api.route('/<string:review_id>')
@api.param('review_id', 'The review identifier')
class ReviewResource(Resource):
    @api.doc('get_review')
    @api.marshal_with(review_model)
    def get(self, review_id):
        """Get a review by ID (public endpoint)"""
        review = reviews_storage.get(review_id)
        if not review:
            api.abort(404, 'Review not found')
        return review.to_dict()

    @api.doc('update_review')
    @api.expect(review_update_model)
    @api.marshal_with(review_model)
    @jwt_required()
    def put(self, review_id):
        """Update a review (reviewer or admin only)"""
        review = reviews_storage.get(review_id)
        if not review:
            api.abort(404, 'Review not found')
        
        # Check if current user can modify this review
        if not can_modify_review(review):
            api.abort(403, 'You can only modify your own reviews')
        
        try:
            data = request.get_json()
            
            # Update review
            review.update(data)
            
            return review.to_dict()
            
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, f'Internal server error: {str(e)}')

    @api.doc('delete_review')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review (reviewer or admin only)"""
        review = reviews_storage.get(review_id)
        if not review:
            api.abort(404, 'Review not found')
        
        # Check if current user can modify this review
        if not can_modify_review(review):
            api.abort(403, 'You can only delete your own reviews')
        
        del reviews_storage[review_id]
        return '', 204
