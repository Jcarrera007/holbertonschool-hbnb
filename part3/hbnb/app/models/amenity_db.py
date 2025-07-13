"""
SQLAlchemy Amenity model for the HBnB application.

This module defines the Amenity entity as a SQLAlchemy model with
database mapping and relationships.
"""

from sqlalchemy import Column, String, Table
from sqlalchemy.orm import relationship
from app.models.base_model_db import BaseModelDB


class AmenityDB(BaseModelDB):
    """
    SQLAlchemy Amenity model.
    
    Represents an amenity in the database that can be associated with places.
    """
    
    __tablename__ = 'amenities'
    
    # Amenity columns
    name = Column(String(50), nullable=False, unique=True)
    
    # Relationships (many-to-many with places)
    # places = relationship("PlaceDB", secondary="place_amenity", back_populates="amenities")
    
    def __init__(self, name, **kwargs):
        """
        Initialize a new Amenity instance.
        
        Args:
            name (str): Amenity name (must be unique)
        """
        super().__init__(**kwargs)
        self.name = name
        
        # Validate inputs
        self._validate()
    
    def _validate(self):
        """Validate amenity attributes."""
        if not self.name or len(self.name.strip()) == 0:
            raise ValueError("Amenity name is required")
        
        if len(self.name) > 50:
            raise ValueError("Amenity name must be 50 characters or less")
    
    def update(self, data):
        """
        Update amenity attributes with validation.
        
        Args:
            data (dict): Dictionary containing attribute names and new values
        """
        # Store old values for validation rollback if needed
        old_values = {}
        for key in data:
            if hasattr(self, key):
                old_values[key] = getattr(self, key)
        
        # Update attributes
        protected_fields = {'id', 'created_at', 'updated_at'}
        for key, value in data.items():
            if hasattr(self, key) and key not in protected_fields:
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
    def find_by_name(cls, name):
        """
        Find an amenity by name.
        
        Args:
            name (str): Name of the amenity
            
        Returns:
            AmenityDB: Amenity instance if found, None otherwise
        """
        from app import db
        return db.session.query(cls).filter_by(name=name).first()
    
    def __str__(self):
        """String representation of the amenity."""
        return f"[AmenityDB] ({self.id}) {self.name}"
