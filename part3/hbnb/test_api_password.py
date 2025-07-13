#!/usr/bin/env python3
"""
Test script to verify the User API with password functionality.
"""

import requests
import json
import time

def test_user_api_with_password():
    """Test the User API endpoints with password functionality."""
    print("🌐 Testing User API with Password Functionality")
    print("=" * 55)
    
    base_url = "http://127.0.0.1:5000/api/v1/users"
    
    # Test data
    user_data = {
        "first_name": "Alice",
        "last_name": "Johnson",
        "email": "alice.johnson@example.com",
        "password": "securepassword123",
        "is_admin": False
    }
    
    try:
        print("1. Testing user creation with password...")
        response = requests.post(base_url + "/", json=user_data)
        
        if response.status_code == 201:
            created_user = response.json()
            user_id = created_user['id']
            print(f"   ✅ User created successfully (ID: {user_id})")
            print(f"   - Password excluded from response: {'password' not in created_user}")
            print(f"   - Response fields: {list(created_user.keys())}")
        else:
            print(f"   ❌ User creation failed: {response.status_code} - {response.text}")
            return False
        
        print("\n2. Testing user retrieval...")
        response = requests.get(f"{base_url}/{user_id}")
        
        if response.status_code == 200:
            retrieved_user = response.json()
            print(f"   ✅ User retrieved successfully")
            print(f"   - Password excluded from response: {'password' not in retrieved_user}")
            print(f"   - Email matches: {retrieved_user['email'] == user_data['email']}")
        else:
            print(f"   ❌ User retrieval failed: {response.status_code} - {response.text}")
            return False
        
        print("\n3. Testing user update with password change...")
        update_data = {
            "first_name": "Alice Updated",
            "password": "newpassword456"
        }
        response = requests.put(f"{base_url}/{user_id}", json=update_data)
        
        if response.status_code == 200:
            updated_user = response.json()
            print(f"   ✅ User updated successfully")
            print(f"   - Name updated: {updated_user['first_name'] == 'Alice Updated'}")
            print(f"   - Password still excluded: {'password' not in updated_user}")
        else:
            print(f"   ❌ User update failed: {response.status_code} - {response.text}")
            return False
        
        print("\n4. Testing duplicate email validation...")
        duplicate_user = {
            "first_name": "Bob",
            "last_name": "Smith",
            "email": "alice.johnson@example.com",  # Same email
            "password": "password123"
        }
        response = requests.post(base_url + "/", json=duplicate_user)
        
        if response.status_code == 400:
            print(f"   ✅ Duplicate email rejected correctly")
        else:
            print(f"   ❌ Duplicate email validation failed: {response.status_code}")
            return False
        
        print("\n5. Testing password validation...")
        short_password_user = {
            "first_name": "Bob",
            "last_name": "Smith",
            "email": "bob.smith@example.com",
            "password": "123"  # Too short
        }
        response = requests.post(base_url + "/", json=short_password_user)
        
        if response.status_code == 400 and "6 characters" in response.text:
            print(f"   ✅ Short password rejected correctly")
        else:
            print(f"   ❌ Password validation failed: {response.status_code} - {response.text}")
            return False
        
        print("\n🎉 SUCCESS: All User API password tests passed!")
        return True
        
    except requests.exceptions.ConnectionError:
        print("   ❌ Cannot connect to server. Please start the application first:")
        print("      python3 run.py")
        return False
    except Exception as e:
        print(f"   ❌ Test failed with error: {e}")
        return False

def start_server_and_test():
    """Start the server and run tests."""
    import subprocess
    import threading
    import os
    
    print("Starting Flask server...")
    
    # Change to the correct directory
    os.chdir('/home/zekki/holbertonschool-hbnb/part3/hbnb')
    
    # Start server in background
    def run_server():
        subprocess.run(['/home/zekki/holbertonschool-hbnb/part3/hbnb/venv/bin/python3', 'run.py'], 
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Wait a moment for server to start
    time.sleep(3)
    
    # Run tests
    return test_user_api_with_password()

if __name__ == '__main__':
    success = start_server_and_test()
    exit(0 if success else 1)
