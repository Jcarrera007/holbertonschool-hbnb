from flask import Flask
from flask_restx import Api

def create_app():
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')

    # Register API namespaces
    from app.api.v1 import register_namespaces
    register_namespaces(api)

    return app