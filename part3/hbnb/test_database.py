#!/usr/bin/env python3
"""
Simple test script for SQLAlchemy database initialization.
"""

import os
import sys

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db

def test_db_connection():
    """Test basic database connection and table creation."""
    print("=== Testing Database Connection ===\n")
    
    # Create app with development config
    app = create_app('development')
    
    with app.app_context():
        try:
            # Try to create all tables
            print("Creating tables...")
            db.create_all()
            print("✓ Tables created successfully!")
            
            # List all tables
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"✓ Found {len(tables)} tables: {tables}")
            
            print("\n=== Database test completed successfully! ===")
            return True
            
        except Exception as e:
            print(f"✗ Database test failed: {e}")
            return False

if __name__ == '__main__':
    success = test_db_connection()
    exit(0 if success else 1)
