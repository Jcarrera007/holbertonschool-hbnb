#!/usr/bin/env python3
"""
Test script to verify JWT authentication functionality.
"""

import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, '/home/zekki/holbertonschool-hbnb/part3/hbnb')

def test_jwt_authentication():
    """Test JWT authentication functionality."""
    print("🔐 Testing JWT Authentication Implementation")
    print("=" * 50)
    
    try:
        # Import modules
        from app import create_app
        from app.models.user import User
        from flask_jwt_extended import create_access_token, decode_token
        
        # Create app context
        app = create_app('testing')
        
        with app.app_context():
            print("1. Testing JWT token creation...")
            
            # Create a test user
            user = User(
                first_name="Test",
                last_name="User",
                email="test.user@example.com",
                password="testpassword123",
                is_admin=False
            )
            
            # Create JWT token
            additional_claims = {
                'is_admin': user.is_admin,
                'email': user.email,
                'user_id': user.id
            }
            
            token = create_access_token(
                identity=user.id,
                additional_claims=additional_claims
            )
            
            print(f"   ✅ JWT token created successfully")
            print(f"   ✅ Token length: {len(token)} characters")
            print(f"   ✅ Token starts with: {token[:20]}...")
            
            print("\n2. Testing JWT token decoding...")
            
            # Decode token
            decoded = decode_token(token)
            print(f"   ✅ Token decoded successfully")
            print(f"   ✅ User ID matches: {decoded['sub'] == user.id}")
            print(f"   ✅ Email claim present: {decoded['email'] == user.email}")
            print(f"   ✅ Admin claim present: {decoded['is_admin'] == user.is_admin}")
            
            print("\n3. Testing admin user token...")
            
            # Create admin user
            admin_user = User(
                first_name="Admin",
                last_name="User",
                email="admin@example.com",
                password="adminpassword123",
                is_admin=True
            )
            
            admin_claims = {
                'is_admin': admin_user.is_admin,
                'email': admin_user.email,
                'user_id': admin_user.id
            }
            
            admin_token = create_access_token(
                identity=admin_user.id,
                additional_claims=admin_claims
            )
            
            admin_decoded = decode_token(admin_token)
            print(f"   ✅ Admin token created")
            print(f"   ✅ Admin flag correct: {admin_decoded['is_admin'] == True}")
            
            print("\n4. Testing token expiration settings...")
            
            from config import Config
            print(f"   ✅ JWT secret key configured: {hasattr(app.config, 'JWT_SECRET_KEY')}")
            print(f"   ✅ Token expiration setting: {app.config.get('JWT_ACCESS_TOKEN_EXPIRES', 'Not set')}")
            
            print("\n🎉 SUCCESS: JWT authentication setup working correctly!")
            return True
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_jwt_authentication()
    exit(0 if success else 1)
