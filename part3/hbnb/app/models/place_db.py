"""
SQLAlchemy Place model for the HBnB application.

This module defines the Place entity as a SQLAlchemy model with
database mapping and relationships.
"""

from sqlalchemy import Column, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base_model_db import BaseModelDB


class PlaceDB(BaseModelDB):
    """
    SQLAlchemy Place model.
    
    Represents a place/property in the database with location and amenity information.
    """
    
    __tablename__ = 'places'
    
    # Place columns
    title = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
    # Foreign key to user (owner)
    owner_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    
    # Relationships
    # owner = relationship("UserDB", back_populates="places")
    # reviews = relationship("ReviewDB", back_populates="place", cascade="all, delete-orphan")
    # amenities = relationship("AmenityDB", secondary="place_amenity", back_populates="places")
    
    def __init__(self, title, description, price, latitude, longitude, owner_id, **kwargs):
        """
        Initialize a new Place instance.
        
        Args:
            title (str): Place title
            description (str): Place description
            price (float): Price per night
            latitude (float): Latitude coordinate
            longitude (float): Longitude coordinate
            owner_id (str): ID of the user who owns this place
        """
        super().__init__(**kwargs)
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        
        # Validate inputs
        self._validate()
    
    def _validate(self):
        """Validate place attributes."""
        if not self.title or len(self.title.strip()) == 0:
            raise ValueError("Title is required")
        
        if len(self.title) > 100:
            raise ValueError("Title must be 100 characters or less")
        
        if self.price <= 0:
            raise ValueError("Price must be a positive number")
        
        if not (-90 <= self.latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        
        if not (-180 <= self.longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180")
    
    def update(self, data):
        """
        Update place attributes with validation.
        
        Args:
            data (dict): Dictionary containing attribute names and new values
        """
        # Store old values for validation rollback if needed
        old_values = {}
        for key in data:
            if hasattr(self, key):
                old_values[key] = getattr(self, key)
        
        # Update attributes
        for key, value in data.items():
            if hasattr(self, key) and key not in {'id', 'created_at', 'updated_at', 'owner_id'}:
                setattr(self, key, value)
        
        try:
            # Validate the updated object
            self._validate()
            # Save if validation passes
            self.save()
        except ValueError:
            # Rollback changes if validation fails
            for key, value in old_values.items():
                setattr(self, key, value)
            raise
    
    @classmethod
    def find_by_owner(cls, owner_id):
        """
        Find all places owned by a specific user.
        
        Args:
            owner_id (str): ID of the owner
            
        Returns:
            list: List of PlaceDB instances
        """
        from app import db
        return db.session.query(cls).filter_by(owner_id=owner_id).all()
    
    def __str__(self):
        """String representation of the place."""
        return f"[PlaceDB] ({self.id}) {self.title} - ${self.price}/night"
