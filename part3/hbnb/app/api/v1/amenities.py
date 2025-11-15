"""
Amenity API endpoints for the HBnB application.

This module defines the RESTful API endpoints for amenity management.
"""

from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt
from app.models.amenity import Amenity

# Create namespace for amenity endpoints
api = Namespace('amenities', description='Amenity operations')

# Define amenity model for Swagger documentation
amenity_model = api.model('Amenity', {
    'id': fields.String(readonly=True, description='The amenity unique identifier'),
    'name': fields.String(required=True, description='Amenity name', max_length=50),
    'created_at': fields.String(readonly=True, description='Creation timestamp'),
    'updated_at': fields.String(readonly=True, description='Last update timestamp')
})

amenity_input_model = api.model('AmenityInput', {
    'name': fields.String(required=True, description='Amenity name', max_length=50)
})

# In-memory storage for demonstration
amenities_storage = {}


def is_admin():
    """Check if the current user is an admin."""
    claims = get_jwt()
    return claims.get('is_admin', False)


@api.route('/')
class AmenityList(Resource):
    @api.doc('list_amenities')
    @api.marshal_list_with(amenity_model)
    def get(self):
        """Get all amenities (public endpoint)"""
        return list(amenities_storage.values())

    @api.doc('create_amenity')
    @api.expect(amenity_input_model)
    @api.marshal_with(amenity_model, code=201)
    @jwt_required()
    def post(self):
        """Create a new amenity (admin only)"""
        try:
            # Only admins can create amenities
            if not is_admin():
                api.abort(403, 'Admin privileges required to create amenities')
            
            data = request.get_json()
            
            # Check if amenity name already exists
            for amenity in amenities_storage.values():
                if amenity.name.lower() == data.get('name', '').lower():
                    api.abort(400, 'Amenity name already exists')
            
            # Create new amenity
            amenity = Amenity(name=data['name'])
            
            # Store amenity
            amenities_storage[amenity.id] = amenity
            
            return amenity.to_dict(), 201
            
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, f'Internal server error: {str(e)}')


@api.route('/<string:amenity_id>')
@api.param('amenity_id', 'The amenity identifier')
class AmenityResource(Resource):
    @api.doc('get_amenity')
    @api.marshal_with(amenity_model)
    def get(self, amenity_id):
        """Get an amenity by ID"""
        amenity = amenities_storage.get(amenity_id)
        if not amenity:
            api.abort(404, 'Amenity not found')
        return amenity.to_dict()

    @api.doc('update_amenity')
    @api.expect(amenity_input_model)
    @api.marshal_with(amenity_model)
    @jwt_required()
    def put(self, amenity_id):
        """Update an amenity (admin only)"""
        # Only admins can update amenities
        if not is_admin():
            api.abort(403, 'Admin privileges required to update amenities')
            
        amenity = amenities_storage.get(amenity_id)
        if not amenity:
            api.abort(404, 'Amenity not found')
        
        try:
            data = request.get_json()
            
            # Check if amenity name already exists (if changing name)
            if 'name' in data and data['name'].lower() != amenity.name.lower():
                for existing_amenity in amenities_storage.values():
                    if existing_amenity.name.lower() == data['name'].lower():
                        api.abort(400, 'Amenity name already exists')
            
            # Update amenity
            amenity.update(data)
            
            return amenity.to_dict()
            
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, f'Internal server error: {str(e)}')

    @api.doc('delete_amenity')
    @jwt_required()
    def delete(self, amenity_id):
        """Delete an amenity (admin only)"""
        # Only admins can delete amenities
        if not is_admin():
            api.abort(403, 'Admin privileges required to delete amenities')
            
        amenity = amenities_storage.get(amenity_id)
        if not amenity:
            api.abort(404, 'Amenity not found')
        
        del amenities_storage[amenity_id]
        return '', 204
