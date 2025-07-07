"""
Review API endpoints for the HBnB application.

This module defines the RESTful API endpoints for review management.
"""

from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
import uuid
from datetime import datetime

# Simple Review class for demonstration
class Review:
    def __init__(self, text, rating, place, user):
        self.id = str(uuid.uuid4())
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'place_id': self.place.id if self.place else None,
            'user_id': self.user.id if self.user else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

# Create namespace for review endpoints
api = Namespace('reviews', description='Review operations')

# Define review model for Swagger documentation
review_model = api.model('Review', {
    'id': fields.String(readonly=True, description='The review unique identifier'),
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, description='Rating from 1 to 5'),
    'place_id': fields.String(required=True, description='Place ID being reviewed'),
    'user_id': fields.String(readonly=True, description='User ID who wrote the review'),
    'created_at': fields.String(readonly=True, description='Creation timestamp'),
    'updated_at': fields.String(readonly=True, description='Last update timestamp')
})

review_input_model = api.model('ReviewInput', {
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, description='Rating from 1 to 5'),
    'place_id': fields.String(required=True, description='Place ID being reviewed')
})

# In-memory storage for demonstration (will be replaced with persistence layer)
reviews_storage = {}


@api.route('/')
class ReviewList(Resource):
    @api.doc('list_reviews')
    @api.marshal_list_with(review_model)
    def get(self):
        """Get all reviews"""
        return [review.to_dict() for review in reviews_storage.values()]

    @api.doc('create_review')
    @api.expect(review_input_model)
    @api.marshal_with(review_model, code=201)
    @jwt_required()
    def post(self):
        """Create a new review"""
        # Get current user from JWT token
        current_user_id = get_jwt_identity()
        
        try:
            data = request.get_json()
            
            # Get user and place from storage
            from .users import users_storage
            from .places import places_storage
            
            user = users_storage.get(current_user_id)
            if not user:
                api.abort(404, 'User not found')
            
            place = places_storage.get(data['place_id'])
            if not place:
                api.abort(404, 'Place not found')
            
            # Check if user is trying to review their own place
            if place.owner.id == current_user_id:
                return {'error': 'You cannot review your own place'}, 400
            
            # Check if user has already reviewed this place
            for review in reviews_storage.values():
                if review.user.id == current_user_id and review.place.id == data['place_id']:
                    return {'error': 'You have already reviewed this place'}, 400
            
            # Create new review
            review = Review(
                text=data['text'],
                rating=data['rating'],
                place=place,
                user=user
            )
            
            # Store the review
            reviews_storage[review.id] = review
            
            # Add review to place
            place.add_review(review)
            
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
        """Get a review by ID"""
        review = reviews_storage.get(review_id)
        if not review:
            api.abort(404, 'Review not found')
        return review.to_dict()

    @api.doc('update_review')
    @api.expect(review_input_model)
    @api.marshal_with(review_model)
    @jwt_required()
    def put(self, review_id):
        """Update a review"""
        # Get current user from JWT token
        current_user_id = get_jwt_identity()
        
        review = reviews_storage.get(review_id)
        if not review:
            api.abort(404, 'Review not found')
        
        # Check if the user is the author of the review
        if review.user.id != current_user_id:
            return {'error': 'Unauthorized action'}, 403
        
        try:
            data = request.get_json()
            
            # Update review (only text and rating, not place_id)
            update_data = {}
            if 'text' in data:
                update_data['text'] = data['text']
            if 'rating' in data:
                update_data['rating'] = data['rating']
            
            review.update(update_data)
            
            return review.to_dict()
            
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, f'Internal server error: {str(e)}')

    @api.doc('delete_review')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        # Get current user from JWT token
        current_user_id = get_jwt_identity()
        
        review = reviews_storage.get(review_id)
        if not review:
            api.abort(404, 'Review not found')
        
        # Check if the user is the author of the review
        if review.user.id != current_user_id:
            return {'error': 'Unauthorized action'}, 403
        
        # Remove review from place
        review.place.remove_review(review)
        
        del reviews_storage[review_id]
        return '', 204


@api.route('/places/<string:place_id>')
@api.param('place_id', 'The place identifier')
class PlaceReviewList(Resource):
    @api.doc('get_place_reviews')
    @api.marshal_list_with(review_model)
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place_reviews = []
        for review in reviews_storage.values():
            if review.place.id == place_id:
                place_reviews.append(review.to_dict())
        return place_reviews
