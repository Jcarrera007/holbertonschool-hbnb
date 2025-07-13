"""
SQLAlchemy Review model for the HBnB application.

This module defines the Review entity as a SQLAlchemy model with
database mapping and relationships.
"""

from sqlalchemy import Column, String, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base_model_db import BaseModelDB


class ReviewDB(BaseModelDB):
    """
    SQLAlchemy Review model.
    
    Represents a review in the database with rating and text content.
    """
    
    __tablename__ = 'reviews'
    
    # Review columns
    text = Column(Text, nullable=False)
    rating = Column(Integer, nullable=False)
    
    # Foreign keys
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    place_id = Column(String(36), ForeignKey('places.id'), nullable=False)
    
    # Relationships
    # user = relationship("UserDB", back_populates="reviews")
    # place = relationship("PlaceDB", back_populates="reviews")
    
    def __init__(self, text, rating, user_id, place_id, **kwargs):
        """
        Initialize a new Review instance.
        
        Args:
            text (str): Review text content
            rating (int): Rating from 1 to 5
            user_id (str): ID of the user who wrote the review
            place_id (str): ID of the place being reviewed
        """
        super().__init__(**kwargs)
        self.text = text
        self.rating = rating
        self.user_id = user_id
        self.place_id = place_id
        
        # Validate inputs
        self._validate()
    
    def _validate(self):
        """Validate review attributes."""
        if not self.text or len(self.text.strip()) == 0:
            raise ValueError("Review text is required")
        
        if not isinstance(self.rating, int) or not (1 <= self.rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")
    
    def update(self, data):
        """
        Update review attributes with validation.
        
        Args:
            data (dict): Dictionary containing attribute names and new values
        """
        # Store old values for validation rollback if needed
        old_values = {}
        for key in data:
            if hasattr(self, key):
                old_values[key] = getattr(self, key)
        
        # Update attributes (protect foreign keys and system fields)
        protected_fields = {'id', 'created_at', 'updated_at', 'user_id', 'place_id'}
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
    def find_by_place(cls, place_id):
        """
        Find all reviews for a specific place.
        
        Args:
            place_id (str): ID of the place
            
        Returns:
            list: List of ReviewDB instances
        """
        from app import db
        return db.session.query(cls).filter_by(place_id=place_id).all()
    
    @classmethod
    def find_by_user(cls, user_id):
        """
        Find all reviews by a specific user.
        
        Args:
            user_id (str): ID of the user
            
        Returns:
            list: List of ReviewDB instances
        """
        from app import db
        return db.session.query(cls).filter_by(user_id=user_id).all()
    
    @classmethod
    def find_by_user_and_place(cls, user_id, place_id):
        """
        Find a review by a specific user for a specific place.
        
        Args:
            user_id (str): ID of the user
            place_id (str): ID of the place
            
        Returns:
            ReviewDB: Review instance if found, None otherwise
        """
        from app import db
        return db.session.query(cls).filter_by(user_id=user_id, place_id=place_id).first()
    
    def __str__(self):
        """String representation of the review."""
        return f"[ReviewDB] ({self.id}) Rating: {self.rating}/5 - {self.text[:50]}..."
