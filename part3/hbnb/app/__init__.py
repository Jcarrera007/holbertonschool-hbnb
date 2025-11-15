from flask import Flask, jsonify
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

# Initialize extensions
bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()

def create_app(config_name='development'):
    """
    Application Factory pattern implementation.
    
    Args:
        config_name (str): The configuration name to use ('development', 'production', etc.)
    
    Returns:
        Flask: The configured Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    from config import config
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    
    # Import models to register them with SQLAlchemy
    from app.models import UserDB, PlaceDB, ReviewDB, AmenityDB
    
    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({'error': 'Token has expired'}), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({'error': 'Invalid token'}), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({'error': 'Access token is required'}), 401
    
    # Initialize API
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')

    # Register API namespaces
    from app.api.v1 import register_namespaces
    register_namespaces(api)

    return app