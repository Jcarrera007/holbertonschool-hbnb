"""
SQLAlchemy User model for the HBnB application.

This module defines the User entity as a SQLAlchemy model with
database mapping and relationships.
"""

from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from app import db, bcrypt
import uuid
from datetime import datetime


class UserDB(db.Model):
    """
    SQLAlchemy User model.
    
    Represents a user in the database with authentication and profile information.
    """
    
    __tablename__ = 'users'
    
    # User columns
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password_hash = Column(String(128), nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships (will be defined when we create related models)
    # places = relationship("PlaceDB", back_populates="owner", cascade="all, delete-orphan")
    # reviews = relationship("ReviewDB", back_populates="user", cascade="all, delete-orphan")
    
    def __init__(self, first_name, last_name, email, password, is_admin=False, **kwargs):
        """
        Initialize a new User instance.
        
        Args:
            first_name (str): User's first name
            last_name (str): User's last name
            email (str): User's email address (unique)
            password (str): User's plain text password (will be hashed)
            is_admin (bool): Whether the user has admin privileges
        """
        super().__init__(**kwargs)
        self.id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.set_password(password)
        self.is_admin = is_admin
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def set_password(self, password):
        """
        Hash and set the user's password.
        
        Args:
            password (str): Plain text password
            
        Raises:
            ValueError: If password is too short
        """
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """
        Check if the provided password matches the user's password.
        
        Args:
            password (str): Plain text password to check
            
        Returns:
            bool: True if password matches, False otherwise
        """
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def save(self):
        """Save the object to the database and update timestamp."""
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()
    
    def to_dict(self):
        """
        Convert the user to a dictionary representation.
        Excludes the password hash for security.
        
        Returns:
            dict: Dictionary containing user attributes (excluding password)
        """
        result = {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        return result
    
    def update(self, data):
        """
        Update user attributes.
        Special handling for password updates.
        
        Args:
            data (dict): Dictionary containing attribute names and new values
        """
        # Handle password updates specially
        if 'password' in data:
            self.set_password(data.pop('password'))
        
        # Update other attributes
        protected_attributes = {'id', 'created_at', 'updated_at'}
        for key, value in data.items():
            if key not in protected_attributes and hasattr(self, key):
                setattr(self, key, value)
        
        self.save()
    
    @classmethod
    def find_by_email(cls, email):
        """
        Find a user by email address.
        
        Args:
            email (str): Email address to search for
            
        Returns:
            UserDB: User instance if found, None otherwise
        """
        return cls.query.filter_by(email=email).first()
    
    def __str__(self):
        """String representation of the user."""
        return f"[UserDB] ({self.id}) {self.first_name} {self.last_name} <{self.email}>"
