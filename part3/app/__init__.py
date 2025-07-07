from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager

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

    # Load configuration (we'll use a simple config for now)
    app.config['SECRET_KEY'] = 'default_secret_key'
    app.config['DEBUG'] = True
    app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'  # Change this in production
    
    # Initialize JWT
    jwt = JWTManager(app)
    
    # Initialize Flask-RESTx API
    api = Api(
        app, 
        version='1.0', 
        title='HBnB API', 
        description='HBnB Application API', 
        doc='/api/v1/'
    )

    # Register API namespaces
    from api.v1 import register_namespaces
    register_namespaces(api)

    return app