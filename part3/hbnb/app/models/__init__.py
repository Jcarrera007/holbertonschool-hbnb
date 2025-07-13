"""
HBnB Models Package

This package contains all the business logic models for the HBnB application.
It includes the base model class and all entity classes with their relationships.
"""

from .base_model import BaseModel
from .user import User
from .amenity import Amenity
from .place import Place
from .review import Review

# SQLAlchemy models
from .base_model_db import BaseModelDB
from .user_db import UserDB
from .amenity_db import AmenityDB
from .place_db import PlaceDB
from .review_db import ReviewDB

# Import and setup relationships
from .relationships import setup_relationships
setup_relationships()

__all__ = [
    'BaseModel',
    'User', 
    'Amenity',
    'Place',
    'Review',
    'BaseModelDB',
    'UserDB',
    'AmenityDB',
    'PlaceDB',
    'ReviewDB'
]
