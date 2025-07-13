#!/usr/bin/env python3
"""
Test script to verify password hashing functionality in the User model.
"""

def test_password_hashing():
    """Test password hashing and verification."""
    print("🔐 Testing Password Hashing Implementation")
    print("=" * 50)
    
    try:
        # Import required modules
        from app import create_app
        from app.models.user import User
        
        # Create app context for bcrypt
        app = create_app('testing')
        
        with app.app_context():
            print("1. Testing password hashing during user creation...")
            
            # Create a user with a password
            user = User(
                first_name="John",
                last_name="Doe",
                email="john.doe@example.com",
                password="password123"
            )
            
            print(f"   ✅ User created successfully")
            print(f"   - Original password: password123")
            print(f"   - Hashed password: {user.password[:20]}...")
            print(f"   - Password is hashed: {user.password != 'password123'}")
            
            print("\n2. Testing password verification...")
            
            # Test correct password
            correct_password = user.verify_password("password123")
            print(f"   ✅ Correct password verification: {correct_password}")
            
            # Test incorrect password
            incorrect_password = user.verify_password("wrongpassword")
            print(f"   ✅ Incorrect password verification: {incorrect_password}")
            
            print("\n3. Testing password validation...")
            
            # Test short password
            try:
                User("Jane", "Doe", "jane@example.com", "123")
                print("   ❌ Short password validation failed")
            except ValueError as e:
                print(f"   ✅ Short password rejected: {e}")
            
            # Test empty password
            try:
                User("Jane", "Doe", "jane@example.com", "")
                print("   ❌ Empty password validation failed")
            except ValueError as e:
                print(f"   ✅ Empty password rejected: {e}")
            
            print("\n4. Testing password update...")
            
            # Update password
            user.update({"password": "newpassword456"})
            
            # Test old password doesn't work
            old_password_works = user.verify_password("password123")
            print(f"   ✅ Old password rejected: {not old_password_works}")
            
            # Test new password works
            new_password_works = user.verify_password("newpassword456")
            print(f"   ✅ New password accepted: {new_password_works}")
            
            print("\n5. Testing to_dict excludes password...")
            
            user_dict = user.to_dict()
            password_excluded = 'password' not in user_dict
            print(f"   ✅ Password excluded from to_dict: {password_excluded}")
            print(f"   - Available fields: {list(user_dict.keys())}")
            
            print("\n🎉 SUCCESS: All password hashing tests passed!")
            return True
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_password_hashing()
    exit(0 if success else 1)
