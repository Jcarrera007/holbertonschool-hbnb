#!/usr/bin/env python3
"""
Example usage of the Application Factory pattern with different configurations.
"""

import os
from app import create_app

def demonstrate_app_factory():
    """Demonstrate different ways to use the Application Factory."""
    
    print("🏭 Application Factory Pattern Demonstration\n")
    
    # Example 1: Using default configuration
    print("1. Creating app with default configuration:")
    app_default = create_app()
    with app_default.app_context():
        print(f"   - App name: {app_default.name}")
        print(f"   - Debug mode: {app_default.config['DEBUG']}")
        print(f"   - Secret key set: {'SECRET_KEY' in app_default.config}")
    
    # Example 2: Using specific configuration
    print("\n2. Creating app with development configuration:")
    app_dev = create_app('development')
    with app_dev.app_context():
        print(f"   - Debug mode: {app_dev.config['DEBUG']}")
        print(f"   - Database URI: {app_dev.config.get('SQLALCHEMY_DATABASE_URI')}")
    
    # Example 3: Using testing configuration
    print("\n3. Creating app with testing configuration:")
    app_test = create_app('testing')
    with app_test.app_context():
        print(f"   - Testing mode: {app_test.config['TESTING']}")
        print(f"   - Database URI: {app_test.config.get('SQLALCHEMY_DATABASE_URI')}")
    
    # Example 4: Environment variable configuration
    print("\n4. Using environment variables:")
    os.environ['FLASK_ENV'] = 'production'
    config_from_env = os.getenv('FLASK_ENV', 'development')
    app_prod = create_app(config_from_env)
    with app_prod.app_context():
        print(f"   - Environment: {config_from_env}")
        print(f"   - Debug mode: {app_prod.config['DEBUG']}")
    
    print("\n✅ Application Factory demonstration complete!")

if __name__ == '__main__':
    demonstrate_app_factory()
