"""
Authentication API endpoints for the HBnB application.

This module defines the RESTful API endpoints for user authentication,
including login and token-based authentication.
"""

from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from app.models.user import User

# Create namespace for auth endpoints
api = Namespace('auth', description='Authentication operations')

# Define models for Swagger documentation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email address'),
    'password': fields.String(required=True, description='User password')
})

token_model = api.model('Token', {
    'access_token': fields.String(description='JWT access token'),
    'user': fields.Raw(description='User information')
})

# In-memory storage for demonstration (same as users.py for now)
# This will be replaced with proper persistence layer
from app.api.v1.users import users_storage


@api.route('/login')
class Login(Resource):
    @api.doc('user_login')
    @api.expect(login_model)
    @api.marshal_with(token_model, code=200)
    def post(self):
        """User login endpoint"""
        try:
            data = request.get_json()
            
            # Validate required fields
            if not data or 'email' not in data or 'password' not in data:
                api.abort(400, 'Email and password are required')
            
            email = data['email'].strip().lower()
            password = data['password']
            
            # Find user by email
            user = None
            for stored_user in users_storage.values():
                if stored_user.email == email:
                    user = stored_user
                    break
            
            if not user:
                api.abort(401, 'Invalid email or password')
            
            # Verify password
            if not user.verify_password(password):
                api.abort(401, 'Invalid email or password')
            
            # Create JWT token with additional claims
            additional_claims = {
                'is_admin': user.is_admin,
                'email': user.email,
                'user_id': user.id
            }
            
            access_token = create_access_token(
                identity=user.id,
                additional_claims=additional_claims
            )
            
            return {
                'access_token': access_token,
                'user': user.to_dict()
            }, 200
            
        except Exception as e:
            if hasattr(e, 'code'):  # Flask-RESTX abort
                raise e
            api.abort(500, f'Internal server error: {str(e)}')


@api.route('/protected')
class ProtectedResource(Resource):
    @api.doc('protected_endpoint')
    @jwt_required()
    def get(self):
        """Protected endpoint to test JWT authentication"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        
        return {
            'message': 'Access granted to protected resource',
            'user_id': current_user_id,
            'is_admin': claims.get('is_admin', False),
            'email': claims.get('email')
        }, 200


@api.route('/me')
class CurrentUser(Resource):
    @api.doc('current_user')
    @jwt_required()
    def get(self):
        """Get current user information from JWT token"""
        current_user_id = get_jwt_identity()
        
        # Find user in storage
        user = users_storage.get(current_user_id)
        if not user:
            api.abort(404, 'User not found')
        
        return user.to_dict(), 200
