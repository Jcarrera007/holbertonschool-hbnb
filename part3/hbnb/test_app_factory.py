#!/usr/bin/env python3
"""
Test script to verify the Application Factory pattern implementation.
"""

from app import create_app
from config import config

def test_app_factory():
    """Test the Application Factory with different configurations."""
    
    # Test development configuration
    app_dev = create_app('development')
    print("✓ Development app created successfully")
    print(f"  - DEBUG: {app_dev.config['DEBUG']}")
    print(f"  - SECRET_KEY: {app_dev.config['SECRET_KEY'][:10]}...")
    print(f"  - DATABASE_URI: {app_dev.config.get('SQLALCHEMY_DATABASE_URI', 'Not set')}")
    
    # Test testing configuration
    app_test = create_app('testing')
    print("\n✓ Testing app created successfully")
    print(f"  - DEBUG: {app_test.config['DEBUG']}")
    print(f"  - TESTING: {app_test.config['TESTING']}")
    print(f"  - DATABASE_URI: {app_test.config.get('SQLALCHEMY_DATABASE_URI', 'Not set')}")
    
    # Test production configuration
    app_prod = create_app('production')
    print("\n✓ Production app created successfully")
    print(f"  - DEBUG: {app_prod.config['DEBUG']}")
    print(f"  - DATABASE_URI: {app_prod.config.get('SQLALCHEMY_DATABASE_URI', 'Not set')}")
    
    # Test default configuration
    app_default = create_app()
    print("\n✓ Default app created successfully")
    print(f"  - DEBUG: {app_default.config['DEBUG']}")
    
    print("\n🎉 All Application Factory tests passed!")

if __name__ == '__main__':
    test_app_factory()
