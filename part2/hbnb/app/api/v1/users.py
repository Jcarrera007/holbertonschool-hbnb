"""
User API endpoints for the HBnB application.

This module defines the RESTful API endpoints for user management.
"""

from flask_restx import Namespace, Resource, fields
from flask import request
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
        """Get a user by ID"""
        user = users_storage.get(user_id)
        if not user:
            api.abort(404, 'User not found')
        return user.to_dict()

    @api.doc('update_user')
    @api.expect(user_input_model)
    @api.marshal_with(user_model)
    def put(self, user_id):
        """Update a user"""
        user = users_storage.get(user_id)
        if not user:
            api.abort(404, 'User not found')
        
        try:
            data = request.get_json()
            
            # Check if email already exists (if changing email)
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
    def delete(self, user_id):
        """Delete a user"""
        user = users_storage.get(user_id)
        if not user:
            api.abort(404, 'User not found')
        
        del users_storage[user_id]
        return '', 204
