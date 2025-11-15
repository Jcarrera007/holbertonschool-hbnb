"""
API v1 package initialization.

This module sets up the Flask-RESTx API v1 namespaces.
"""

from flask_restx import Api
from .users import api as users_ns
from .amenities import api as amenities_ns
from .auth import api as auth_ns

# This will be used to register namespaces with the main API
def register_namespaces(api):
    """Register all v1 namespaces with the API instance."""
    api.add_namespace(users_ns, path='/users')
    api.add_namespace(amenities_ns, path='/amenities')
    api.add_namespace(auth_ns, path='/auth')
