"""
Place API endpoints for the HBnB application.

This module defines the RESTful API endpoints for place management.
"""

from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.models.place import Place

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
    'owner_id': fields.String(required=True, description='Owner user ID'),
    'amenities': fields.List(fields.String, description='List of amenity IDs'),
    'created_at': fields.String(readonly=True, description='Creation timestamp'),
    'updated_at': fields.String(readonly=True, description='Last update timestamp')
})

place_input_model = api.model('PlaceInput', {
    'title': fields.String(required=True, description='Place title', max_length=100),
    'description': fields.String(description='Place description'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude coordinate'),
    'longitude': fields.Float(required=True, description='Longitude coordinate'),
    'amenities': fields.List(fields.String, description='List of amenity IDs')
})

place_update_model = api.model('PlaceUpdate', {
    'title': fields.String(description='Place title', max_length=100),
    'description': fields.String(description='Place description'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude coordinate'),
    'longitude': fields.Float(description='Longitude coordinate'),
    'amenities': fields.List(fields.String, description='List of amenity IDs')
})

# In-memory storage for demonstration
places_storage = {}


def is_admin():
    """Check if the current user is an admin."""
    claims = get_jwt()
    return claims.get('is_admin', False)


def can_modify_place(place):
    """Check if current user can modify the place."""
    current_user_id = get_jwt_identity()
    
    # Admin can modify any place
    if is_admin():
        return True
    
    # Owner can modify their own place
    return place.owner_id == current_user_id


@api.route('/')
class PlaceList(Resource):
    @api.doc('list_places')
    @api.marshal_list_with(place_model)
    def get(self):
        """Get all places (public endpoint)"""
        return list(places_storage.values())

    @api.doc('create_place')
    @api.expect(place_input_model)
    @api.marshal_with(place_model, code=201)
    @jwt_required()
    def post(self):
        """Create a new place (authenticated users only)"""
        try:
            data = request.get_json()
            current_user_id = get_jwt_identity()
            
            # Validate required fields
            required_fields = ['title', 'price', 'latitude', 'longitude']
            for field in required_fields:
                if field not in data:
                    api.abort(400, f'{field} is required')
            
            # Create new place with current user as owner
            place = Place(
                title=data['title'],
                description=data.get('description', ''),
                price=data['price'],
                latitude=data['latitude'],
                longitude=data['longitude'],
                owner_id=current_user_id,
                amenities=data.get('amenities', [])
            )
            
            # Store place
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
    @api.expect(place_update_model)
    @api.marshal_with(place_model)
    @jwt_required()
    def put(self, place_id):
        """Update a place (owner or admin only)"""
        place = places_storage.get(place_id)
        if not place:
            api.abort(404, 'Place not found')
        
        # Check if current user can modify this place
        if not can_modify_place(place):
            api.abort(403, 'You can only modify your own places')
        
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
        """Delete a place (owner or admin only)"""
        place = places_storage.get(place_id)
        if not place:
            api.abort(404, 'Place not found')
        
        # Check if current user can modify this place
        if not can_modify_place(place):
            api.abort(403, 'You can only delete your own places')
        
        del places_storage[place_id]
        return '', 204
