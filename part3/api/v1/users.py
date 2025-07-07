"""
User API endpoints for the HBnB application.

This module defines the RESTful API endpoints for user management.
"""

from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
import uuid
from datetime import datetime

# Simple User class for demonstration
class User:
    def __init__(self, first_name, last_name, email, is_admin=False, password=None):
        self.id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.password = password
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def verify_password(self, password):
        return self.password == password
    
    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

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
    'password': fields.String(required=True, description='User password'),
    'is_admin': fields.Boolean(description='Admin privileges', default=False)
})

# In-memory storage for demonstration (will be replaced with persistence layer)
users_storage = {}


@api.route('/')
class UserList(Resource):
    @api.doc('list_users')
    @api.marshal_list_with(user_model)
    def get(self):
        """Get all users"""
        return list(users_storage.values())

    @api.doc('create_user')
    @api.expect(user_input_model)
    @api.marshal_with(user_model, code=201)
    def post(self):
        """Create a new user"""
        try:
            data = request.get_json()
            
            # Check if email already exists
            for user in users_storage.values():
                if user.email == data.get('email'):
                    api.abort(400, 'Email already exists')
            
            # Create new user
            user = User(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                is_admin=data.get('is_admin', False),
                password=data.get('password')  # Include password
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
        """Get a user by ID"""
        user = users_storage.get(user_id)
        if not user:
            api.abort(404, 'User not found')
        return user.to_dict()

    @api.doc('update_user')
    @api.expect(user_input_model)
    @api.marshal_with(user_model)
    @jwt_required()
    def put(self, user_id):
        """Update a user"""
        # Get current user from JWT token
        current_user_id = get_jwt_identity()
        
        # Check if the user is trying to modify their own data
        if current_user_id != user_id:
            return {'error': 'Unauthorized action'}, 403
        
        user = users_storage.get(user_id)
        if not user:
            api.abort(404, 'User not found')
        
        try:
            data = request.get_json()
            
            # Prevent modification of email and password
            if 'email' in data or 'password' in data:
                return {'error': 'You cannot modify email or password'}, 400
            
            # Update user
            user.update(data)
            
            return user.to_dict()
            
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, f'Internal server error: {str(e)}')

    @api.doc('delete_user')
    def delete(self, user_id):
        """Delete a user"""
        user = users_storage.get(user_id)
        if not user:
            api.abort(404, 'User not found')
        
        del users_storage[user_id]
        return '', 204
