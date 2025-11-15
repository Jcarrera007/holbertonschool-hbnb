"""
SQLAlchemy relationships and association tables for the HBnB application.

This module defines the relationships between entities and association tables
for many-to-many relationships.
"""

from sqlalchemy import Table, Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base_model_db import Base

# Association table for the many-to-many relationship between Place and Amenity
place_amenity = Table(
    'place_amenity',
    Base.metadata,
    Column('place_id', String(36), ForeignKey('places.id'), primary_key=True),
    Column('amenity_id', String(36), ForeignKey('amenities.id'), primary_key=True)
)

# Import models after defining the association table to avoid circular imports
def setup_relationships():
    """Setup relationships between models after all models are defined."""
    from app.models.user_db import UserDB
    from app.models.place_db import PlaceDB
    from app.models.review_db import ReviewDB
    from app.models.amenity_db import AmenityDB
    
    # User relationships
    UserDB.places = relationship("PlaceDB", back_populates="owner", cascade="all, delete-orphan")
    UserDB.reviews = relationship("ReviewDB", back_populates="user", cascade="all, delete-orphan")

    # Place relationships
    PlaceDB.owner = relationship("UserDB", back_populates="places")
    PlaceDB.reviews = relationship("ReviewDB", back_populates="place", cascade="all, delete-orphan")
    PlaceDB.amenities = relationship("AmenityDB", secondary=place_amenity, back_populates="places")

    # Review relationships
    ReviewDB.user = relationship("UserDB", back_populates="reviews")
    ReviewDB.place = relationship("PlaceDB", back_populates="reviews")

    # Amenity relationships
    AmenityDB.places = relationship("PlaceDB", secondary=place_amenity, back_populates="amenities")
