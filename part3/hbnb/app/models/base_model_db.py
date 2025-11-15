"""
SQLAlchemy base model for all HBnB entities.

This module provides the SQLAlchemy base model that integrates with
our existing BaseModel for database persistence.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

# Create the declarative base
Base = declarative_base()


class BaseModelDB(Base):
    """
    SQLAlchemy base model for all HBnB entities.
    
    This class provides the database structure and common functionality
    for all models that need to be persisted in the database.
    """
    
    __abstract__ = True  # This ensures SQLAlchemy doesn't create a table for this class
    
    # Common columns for all models
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __init__(self, **kwargs):
        """Initialize a new instance with optional keyword arguments."""
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())
        if not self.created_at:
            self.created_at = datetime.utcnow()
        if not self.updated_at:
            self.updated_at = datetime.utcnow()
    
    def save(self):
        """Save the object to the database and update timestamp."""
        from app import db
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()
    
    def update(self, data):
        """
        Update the attributes of the object based on the provided dictionary.
        
        Args:
            data (dict): Dictionary containing attribute names and new values
        """
        protected_attributes = {'id', 'created_at', 'updated_at'}
        
        for key, value in data.items():
            if key not in protected_attributes and hasattr(self, key):
                setattr(self, key, value)
        
        self.save()  # Save to database and update timestamp
    
    def delete(self):
        """Delete the object from the database."""
        from app import db
        db.session.delete(self)
        db.session.commit()
    
    def to_dict(self):
        """
        Convert the object to a dictionary representation.
        
        Returns:
            dict: Dictionary containing all object attributes
        """
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, datetime):
                result[column.name] = value.isoformat()
            else:
                result[column.name] = value
        return result
    
    def __str__(self):
        """String representation of the object."""
        return f"[{self.__class__.__name__}] ({self.id}) {self.to_dict()}"
    
    def __repr__(self):
        """Detailed string representation of the object."""
        return self.__str__()
