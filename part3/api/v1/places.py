"""
Place API endpoints for the HBnB application.

This module defines the RESTful API endpoints for place management.
"""

from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
import uuid
from datetime import datetime

# Simple Place class for demonstration
class Place:
    def __init__(self, title, description, price, latitude, longitude, owner):
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []
        self.amenities = []
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()
    
    def add_review(self, review):
        if review not in self.reviews:
            self.reviews.append(review)
    
    def remove_review(self, review):
        if review in self.reviews:
            self.reviews.remove(review)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner.id if self.owner else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

# Create namespace for place endpoints
api = Namespace('places', description='Place operations')

# Define place model for Swagger documentation
place_model = api.model('Place', {
    'id': fields.String(readonly=True, description='The place unique identifier'),
    'title': fields.String(required=True, description='Place title', max_length=100),
    'description': fields.String(description='Place description'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude coordinate'),
    'longitude': fields.Float(required=True, description='Longitude coordinate'),
    'owner_id': fields.String(readonly=True, description='Owner user ID'),
    'created_at': fields.String(readonly=True, description='Creation timestamp'),
    'updated_at': fields.String(readonly=True, description='Last update timestamp')
})

place_input_model = api.model('PlaceInput', {
    'title': fields.String(required=True, description='Place title', max_length=100),
    'description': fields.String(description='Place description'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude coordinate'),
    'longitude': fields.Float(required=True, description='Longitude coordinate')
})

# In-memory storage for demonstration (will be replaced with persistence layer)
places_storage = {}


@api.route('/')
class PlaceList(Resource):
    @api.doc('list_places')
    @api.marshal_list_with(place_model)
    def get(self):
        """Get all places (public endpoint)"""
        return [place.to_dict() for place in places_storage.values()]

    @api.doc('create_place')
    @api.expect(place_input_model)
    @api.marshal_with(place_model, code=201)
    @jwt_required()
    def post(self):
        """Create a new place"""
        # Get current user from JWT token
        current_user_id = get_jwt_identity()
        
        try:
            data = request.get_json()
            
            # Get owner from users storage
            from .users import users_storage
            owner = users_storage.get(current_user_id)
            if not owner:
                api.abort(404, 'Owner user not found')
            
            # Create new place with owner set to current user
            place = Place(
                title=data['title'],
                description=data.get('description', ''),
                price=data['price'],
                latitude=data['latitude'],
                longitude=data['longitude'],
                owner=owner
            )
            
            # Store the place
            places_storage[place.id] = place
            
            return place.to_dict(), 201
            
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, f'Internal server error: {str(e)}')


@api.route('/<string:place_id>')
@api.param('place_id', 'The place identifier')
class PlaceResource(Resource):
    @api.doc('get_place')
    @api.marshal_with(place_model)
    def get(self, place_id):
        """Get a place by ID (public endpoint)"""
        place = places_storage.get(place_id)
        if not place:
            api.abort(404, 'Place not found')
        return place.to_dict()

    @api.doc('update_place')
    @api.expect(place_input_model)
    @api.marshal_with(place_model)
    @jwt_required()
    def put(self, place_id):
        """Update a place"""
        # Get current user from JWT token
        current_user_id = get_jwt_identity()
        
        place = places_storage.get(place_id)
        if not place:
            api.abort(404, 'Place not found')
        
        # Check if the user is the owner of the place
        if place.owner.id != current_user_id:
            return {'error': 'Unauthorized action'}, 403
        
        try:
            data = request.get_json()
            
            # Update place
            place.update(data)
            
            return place.to_dict()
            
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, f'Internal server error: {str(e)}')

    @api.doc('delete_place')
    @jwt_required()
    def delete(self, place_id):
        """Delete a place"""
        # Get current user from JWT token
        current_user_id = get_jwt_identity()
        
        place = places_storage.get(place_id)
        if not place:
            api.abort(404, 'Place not found')
        
        # Check if the user is the owner of the place
        if place.owner.id != current_user_id:
            return {'error': 'Unauthorized action'}, 403
        
        del places_storage[place_id]
        return '', 204
