#!/usr/bin/env python3
"""
Database initialization script for the HBnB application.

This script creates all database tables using SQLAlchemy models
and optionally populates them with initial data.
"""

import os
import sys
from datetime import datetime

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import (
    UserDB, PlaceDB, ReviewDB, AmenityDB
)
from app import bcrypt


def create_tables():
    """Create all database tables."""
    print("Creating database tables...")
    db.create_all()
    print("✓ Database tables created successfully!")


def populate_initial_data():
    """Populate the database with initial data."""
    print("Populating initial data...")
    
    try:
        # Create admin user
        admin_password_hash = bcrypt.generate_password_hash('admin123').decode('utf-8')
        admin = UserDB(
            first_name='System',
            last_name='Administrator',
            email='admin@hbnb.com',
            password='admin123',  # This will be hashed by the model
            is_admin=True
        )
        db.session.add(admin)
        
        # Create sample amenities
        amenities_data = [
            'WiFi', 'Air Conditioning', 'Swimming Pool', 'Parking',
            'Kitchen', 'TV', 'Heating', 'Balcony'
        ]
        
        amenities = []
        for amenity_name in amenities_data:
            amenity = AmenityDB(name=amenity_name)
            amenities.append(amenity)
            db.session.add(amenity)
        
        # Create sample users
        users_data = [
            ('John', 'Doe', 'john@example.com', 'password123'),
            ('Jane', 'Smith', 'jane@example.com', 'password123'),
            ('Bob', 'Johnson', 'bob@example.com', 'password123')
        ]
        
        users = []
        for first_name, last_name, email, password in users_data:
            user = UserDB(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                is_admin=False
            )
            users.append(user)
            db.session.add(user)
        
        # Commit users and amenities first so they have IDs
        db.session.commit()
        
        # Create sample places
        places_data = [
            {
                'title': 'Cozy Downtown Apartment',
                'description': 'A beautiful 2-bedroom apartment in the heart of the city with modern amenities.',
                'price': 120.50,
                'latitude': 40.7589,
                'longitude': -73.9851,
                'owner': users[0],
                'amenity_names': ['WiFi', 'Air Conditioning', 'Parking', 'Kitchen', 'TV']
            },
            {
                'title': 'Beachfront Villa',
                'description': 'Stunning oceanview villa with private beach access and luxury furnishings.',
                'price': 450.00,
                'latitude': 25.7617,
                'longitude': -80.1918,
                'owner': users[1],
                'amenity_names': ['WiFi', 'Air Conditioning', 'Swimming Pool', 'Parking', 'Kitchen', 'TV', 'Balcony']
            },
            {
                'title': 'Mountain Cabin Retreat',
                'description': 'Peaceful cabin in the mountains, perfect for nature lovers and hiking enthusiasts.',
                'price': 85.75,
                'latitude': 39.7392,
                'longitude': -104.9903,
                'owner': users[0],
                'amenity_names': ['WiFi', 'Kitchen', 'Heating']
            }
        ]
        
        places = []
        for place_data in places_data:
            place = PlaceDB(
                title=place_data['title'],
                description=place_data['description'],
                price=place_data['price'],
                latitude=place_data['latitude'],
                longitude=place_data['longitude'],
                owner_id=place_data['owner'].id
            )
            
            # Add amenities to the place
            for amenity_name in place_data['amenity_names']:
                amenity = next((a for a in amenities if a.name == amenity_name), None)
                if amenity:
                    place.amenities.append(amenity)
            
            places.append(place)
            db.session.add(place)
        
        # Commit places
        db.session.commit()
        
        # Create sample reviews
        reviews_data = [
            {
                'text': 'Amazing place! The location was perfect and the apartment was exactly as described.',
                'rating': 5,
                'user': users[1],
                'place': places[0]
            },
            {
                'text': 'Beautiful villa with incredible ocean views. Would definitely stay again!',
                'rating': 5,
                'user': users[2],
                'place': places[1]
            },
            {
                'text': 'The cabin was cozy and peaceful. Great for a weekend getaway from the city.',
                'rating': 4,
                'user': users[2],
                'place': places[2]
            }
        ]
        
        for review_data in reviews_data:
            review = ReviewDB(
                text=review_data['text'],
                rating=review_data['rating'],
                user_id=review_data['user'].id,
                place_id=review_data['place'].id
            )
            db.session.add(review)
        
        # Final commit
        db.session.commit()
        
        print("✓ Initial data populated successfully!")
        
    except Exception as e:
        print(f"✗ Error populating initial data: {e}")
        db.session.rollback()
        raise


def main():
    """Main function to initialize the database."""
    print("=== HBnB Database Initialization ===\n")
    
    # Create app with development config
    app = create_app('development')
    
    with app.app_context():
        try:
            # Create tables
            create_tables()
            
            # Ask user if they want to populate initial data
            response = input("\nWould you like to populate the database with initial data? (y/n): ")
            if response.lower() in ['y', 'yes']:
                populate_initial_data()
            
            print("\n=== Database initialization completed! ===")
            print(f"Database file: {app.config['SQLALCHEMY_DATABASE_URI']}")
            
        except Exception as e:
            print(f"\n✗ Database initialization failed: {e}")
            return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
