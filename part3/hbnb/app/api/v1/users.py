"""
User API endpoints for the HBnB application.

This module defines the RESTful API endpoints for user management.
"""

from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.models.user import User

# Create namespace for user endpoints
api = Namespace('users', description='User operations')

# Define user model for Swagger documentation
user_model = api.model('User', {
    'id': fields.String(readonly=True, description='The user unique identifier'),
    'first_name': fields.String(required=True, description='User first name', max_length=50),
    'last_name': fields.String(required=True, description='User last name', max_length=50),
    'email': fields.String(required=True, description='User email address'),
    'is_admin': fields.Boolean(description='Admin privileges', default=False),
    'created_at': fields.String(readonly=True, description='Creation timestamp'),
    'updated_at': fields.String(readonly=True, description='Last update timestamp')
})

user_input_model = api.model('UserInput', {
    'first_name': fields.String(required=True, description='User first name', max_length=50),
    'last_name': fields.String(required=True, description='User last name', max_length=50),
    'email': fields.String(required=True, description='User email address'),
    'password': fields.String(required=True, description='User password (min 6 characters)'),
    'is_admin': fields.Boolean(description='Admin privileges', default=False)
})

user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='User first name', max_length=50),
    'last_name': fields.String(description='User last name', max_length=50),
    'email': fields.String(description='User email address'),
    'password': fields.String(description='User password (min 6 characters)'),
    'is_admin': fields.Boolean(description='Admin privileges')
})

# In-memory storage for demonstration (will be replaced with persistence layer)
users_storage = {}


def is_admin():
    """Check if the current user is an admin."""
    claims = get_jwt()
    return claims.get('is_admin', False)


def get_current_user():
    """Get the current user from JWT token."""
    current_user_id = get_jwt_identity()
    return users_storage.get(current_user_id)


def can_modify_user(target_user_id):
    """Check if current user can modify the target user."""
    current_user_id = get_jwt_identity()
    
    # Admin can modify anyone
    if is_admin():
        return True
    
    # Users can only modify themselves
    return current_user_id == target_user_id


@api.route('/')
class UserList(Resource):
    @api.doc('list_users')
    @api.marshal_list_with(user_model)
    def get(self):
        """Get all users (public endpoint)"""
        return list(users_storage.values())

    @api.doc('create_user')
    @api.expect(user_input_model)
    @api.marshal_with(user_model, code=201)
    @jwt_required()
    def post(self):
        """Create a new user (admin only)"""
        try:
            # Only admins can create users
            if not is_admin():
                api.abort(403, 'Admin privileges required to create users')
            
            data = request.get_json()
            
            # Validate required fields
            required_fields = ['first_name', 'last_name', 'email', 'password']
            for field in required_fields:
                if field not in data:
                    api.abort(400, f'{field} is required')
            
            # Check if email already exists
            for user in users_storage.values():
                if user.email == data.get('email'):
                    api.abort(400, 'Email already exists')
            
            # Create new user
            user = User(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                password=data['password'],
                is_admin=data.get('is_admin', False)
            )
            
            # Store user
            users_storage[user.id] = user
            
            return user.to_dict(), 201
            
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, f'Internal server error: {str(e)}')


@api.route('/<string:user_id>')
@api.param('user_id', 'The user identifier')
class UserResource(Resource):
    @api.doc('get_user')
    @api.marshal_with(user_model)
    def get(self, user_id):
        """Get a user by ID (public endpoint)"""
        user = users_storage.get(user_id)
        if not user:
            api.abort(404, 'User not found')
        return user.to_dict()

    @api.doc('update_user')
    @api.expect(user_update_model)
    @api.marshal_with(user_model)
    @jwt_required()
    def put(self, user_id):
        """Update a user (user can update themselves, admin can update anyone)"""
        user = users_storage.get(user_id)
        if not user:
            api.abort(404, 'User not found')
        
        # Check if current user can modify this user
        if not can_modify_user(user_id):
            api.abort(403, 'You can only modify your own profile')
        
        try:
            data = request.get_json()
            
            # Regular users cannot change email or admin status
            current_user_id = get_jwt_identity()
            if current_user_id == user_id and not is_admin():
                # Remove protected fields for regular users updating themselves
                protected_fields = ['email', 'is_admin']
                for field in protected_fields:
                    if field in data:
                        api.abort(403, f'You cannot modify the {field} field')
            
            # Check if email already exists (if changing email and user is admin)
            if 'email' in data and data['email'] != user.email:
                for existing_user in users_storage.values():
                    if existing_user.email == data['email']:
                        api.abort(400, 'Email already exists')
            
            # Update user
            user.update(data)
            
            return user.to_dict()
            
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, f'Internal server error: {str(e)}')

    @api.doc('delete_user')
    @jwt_required()
    def delete(self, user_id):
        """Delete a user (admin only)"""
        # Only admins can delete users
        if not is_admin():
            api.abort(403, 'Admin privileges required to delete users')
        
        user = users_storage.get(user_id)
        if not user:
            api.abort(404, 'User not found')
        
        del users_storage[user_id]
        return '', 204
