"""
Authentication API endpoints for the HBnB application.

This module defines JWT-based authentication endpoints.
"""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.services import facade

# Create namespace for authentication endpoints
api = Namespace('auth', description='Authentication operations')

# Define login model for Swagger documentation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

# Define token response model
token_model = api.model('Token', {
    'access_token': fields.String(description='JWT access token'),
    'message': fields.String(description='Success message')
})

# Define protected response model
protected_model = api.model('ProtectedResponse', {
    'message': fields.String(description='Protected resource message'),
    'user_id': fields.String(description='Current user ID'),
    'is_admin': fields.Boolean(description='Whether user is admin')
})


@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    @api.marshal_with(token_model, code=200)
    @api.doc('user_login')
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = api.payload  # Get the email and password from the request payload
        
        # Step 1: Retrieve the user based on the provided email
        user = facade.get_user_by_email(credentials['email'])
        
        # Step 2: Check if the user exists and the password is correct
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        # Step 3: Create a JWT token with the user's id and is_admin flag
        access_token = create_access_token(
            identity={'id': str(user.id), 'is_admin': user.is_admin}
        )
        
        # Step 4: Return the JWT token to the client
        return {
            'access_token': access_token,
            'message': 'Login successful'
        }, 200


@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    @api.marshal_with(protected_model, code=200)
    @api.doc('protected_endpoint')
    def get(self):
        """A protected endpoint that requires a valid JWT token"""
        current_user = get_jwt_identity()  # Retrieve the user's identity from the token
        return {
            'message': f'Hello, user {current_user["id"]}',
            'user_id': current_user['id'],
            'is_admin': current_user.get('is_admin', False)
        }, 200


@api.route('/admin-only')
class AdminOnlyResource(Resource):
    @jwt_required()
    @api.doc('admin_only_endpoint')
    def get(self):
        """An endpoint that requires admin privileges"""
        current_user = get_jwt_identity()
        
        # Check if the user is an admin
        if not current_user.get('is_admin', False):
            return {'error': 'Admin access required'}, 403
        
        return {
            'message': f'Hello, admin {current_user["id"]}',
            'admin_data': 'This is sensitive admin information'
        }, 200
