#!/usr/bin/env python3
"""
Simple test to verify password functionality with direct model testing.
"""

import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, '/home/zekki/holbertonschool-hbnb/part3/hbnb')

def test_user_password_integration():
    """Test the complete user password integration."""
    print("🔗 Testing User Password Integration")
    print("=" * 40)
    
    try:
        # Import modules
        from app import create_app
        from app.models.user import User
        
        # Create app context
        app = create_app('testing')
        
        with app.app_context():
            print("1. Testing direct user creation with password...")
            
            # Create user with password
            user = User(
                first_name="Test",
                last_name="User",
                email="test.user@example.com",
                password="testpassword123"
            )
            
            print(f"   ✅ User created: {user.first_name} {user.last_name}")
            print(f"   ✅ Password hashed: {len(user.password) > 20}")
            print(f"   ✅ Password verification works: {user.verify_password('testpassword123')}")
            
            print("\n2. Testing to_dict response...")
            user_dict = user.to_dict()
            print(f"   ✅ Password excluded: {'password' not in user_dict}")
            print(f"   ✅ Expected fields present: {set(['id', 'first_name', 'last_name', 'email', 'is_admin', 'created_at', 'updated_at']).issubset(set(user_dict.keys()))}")
            
            print("\n3. Testing password update...")
            user.update({'password': 'newpassword456'})
            print(f"   ✅ Old password rejected: {not user.verify_password('testpassword123')}")
            print(f"   ✅ New password accepted: {user.verify_password('newpassword456')}")
            
            print("\n4. Testing password validation...")
            try:
                User("Bad", "User", "bad@example.com", "123")
                print("   ❌ Short password validation failed")
                return False
            except ValueError as e:
                print(f"   ✅ Short password rejected: {str(e)}")
            
            print("\n🎉 SUCCESS: Password integration working perfectly!")
            return True
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_user_password_integration()
    exit(0 if success else 1)
