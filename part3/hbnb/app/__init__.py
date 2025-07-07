from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# Create bcrypt instance globally to be used across the application
bcrypt = Bcrypt()

# Create JWT manager instance globally
jwt = JWTManager()

def create_app(config_name='development'):
    """
    Create Flask application using the Application Factory pattern.
    
    Args:
        config_name (str): Configuration name ('development', 'production', etc.)
                          Defaults to 'development'
    
    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)

    # Load configuration
    from config import config
    app.config.from_object(config[config_name])
    
    # Initialize bcrypt with the app
    bcrypt.init_app(app)
    
    # Initialize JWT with the app
    jwt.init_app(app)
    
    # Initialize Flask-RESTx API
    api = Api(
        app, 
        version='1.0', 
        title='HBnB API', 
        description='HBnB Application API', 
        doc='/api/v1/'
    )

    # Register API namespaces
    from app.api.v1 import register_namespaces
    register_namespaces(api)

    return app