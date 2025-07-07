"""
Authentication endpoints for the HBnB application.

This module handles user authentication including login.
"""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
import datetime

# Simple in-memory storage for users (in production, use a database)
users_storage = {}

# Import users storage from users module
from .users import users_storage as users_data

api = Namespace('auth', description='Authentication operations')

# Auth request model
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

# Auth response model
token_model = api.model('Token', {
    'access_token': fields.String(description='JWT access token')
})

@api.route('/login')
class AuthLogin(Resource):
    @api.expect(login_model)
    @api.marshal_with(token_model)
    @api.doc('login_user')
    def post(self):
        """Authenticate a user and return a JWT token"""
        data = api.payload
        
        # Validate required fields
        if not data.get('email') or not data.get('password'):
            api.abort(400, 'Email and password are required')
        
        # Find user by email
        user = None
        for user_id, user_obj in users_data.items():
            if user_obj.email == data['email']:
                user = user_obj
                break
        
        if not user:
            api.abort(401, 'Invalid email or password')
        
        # For demo purposes, we're not using hashed passwords
        # In production, you would use check_password_hash
        if user.password != data['password']:
            api.abort(401, 'Invalid email or password')
        
        # Create JWT token
        access_token = create_access_token(
            identity=user.id,
            expires_delta=datetime.timedelta(hours=24)
        )
        
        return {'access_token': access_token}
