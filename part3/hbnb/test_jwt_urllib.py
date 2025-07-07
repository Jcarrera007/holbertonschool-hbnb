#!/usr/bin/env python3
"""
Test JWT Authentication using urllib instead of requests
"""

import json
import urllib.request
import urllib.parse
import urllib.error

BASE_URL = "http://127.0.0.1:5000/api/v1"

def make_request(url, method='GET', data=None, headers=None):
    """Make HTTP request using urllib"""
    if headers is None:
        headers = {'Content-Type': 'application/json'}
    
    if data:
        data = json.dumps(data).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode()), response.getcode()
    except urllib.error.HTTPError as e:
        try:
            error_data = json.loads(e.read().decode())
            return error_data, e.code
        except:
            return {'error': str(e)}, e.code

def test_jwt_auth():
    """Test JWT authentication flow"""
    
    print("Testing JWT Authentication")
    print("=" * 50)
    
    # Step 1: Create a test user
    print("\n1. Creating test user...")
    user_data = {
        "first_name": "John",
        "last_name": "Doe", 
        "email": "john.doe@test.com",
        "password": "securepassword123",
        "is_admin": False
    }
    
    response, status = make_request(f"{BASE_URL}/users/", "POST", user_data)
    print(f"Status: {status}")
    print(f"Response: {response}")
    
    if status != 201:
        print("❌ Failed to create user")
        return
    
    print("✅ User created successfully")
    user_id = response.get('id')
    
    # Step 2: Test login
    print("\n2. Testing login...")
    login_data = {
        "email": "john.doe@test.com",
        "password": "securepassword123"
    }
    
    response, status = make_request(f"{BASE_URL}/auth/login", "POST", login_data)
    print(f"Status: {status}")
    print(f"Response: {response}")
    
    if status != 200:
        print("❌ Login failed")
        return
    
    print("✅ Login successful")
    access_token = response.get('access_token')
    
    if not access_token:
        print("❌ No access token received")
        return
    
    print(f"Token received: {access_token[:50]}...")
    
    # Step 3: Test protected endpoint
    print("\n3. Testing protected endpoint...")
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    response, status = make_request(f"{BASE_URL}/auth/protected", "GET", headers=headers)
    print(f"Status: {status}")
    print(f"Response: {response}")
    
    if status == 200:
        print("✅ Protected endpoint access successful")
    else:
        print("❌ Protected endpoint access failed")
    
    # Step 4: Test invalid token
    print("\n4. Testing with invalid token...")
    headers = {
        'Authorization': 'Bearer invalid_token',
        'Content-Type': 'application/json'
    }
    
    response, status = make_request(f"{BASE_URL}/auth/protected", "GET", headers=headers)
    print(f"Status: {status}")
    print(f"Response: {response}")
    
    if status == 422 or status == 401:
        print("✅ Invalid token correctly rejected")
    else:
        print("❌ Invalid token was not rejected")
    
    # Step 5: Create admin user
    print("\n5. Creating admin user...")
    admin_data = {
        "first_name": "Admin",
        "last_name": "User",
        "email": "admin@test.com", 
        "password": "adminpass123",
        "is_admin": True
    }
    
    response, status = make_request(f"{BASE_URL}/users/", "POST", admin_data)
    print(f"Status: {status}")
    print(f"Response: {response}")
    
    if status != 201:
        print("❌ Failed to create admin user")
        return
    
    print("✅ Admin user created successfully")
    
    # Step 6: Test admin login
    print("\n6. Testing admin login...")
    admin_login = {
        "email": "admin@test.com",
        "password": "adminpass123"
    }
    
    response, status = make_request(f"{BASE_URL}/auth/login", "POST", admin_login)
    print(f"Status: {status}")
    print(f"Response: {response}")
    
    if status != 200:
        print("❌ Admin login failed")
        return
    
    print("✅ Admin login successful")
    admin_token = response.get('access_token')
    
    # Step 7: Test admin-only endpoint
    print("\n7. Testing admin-only endpoint...")
    admin_headers = {
        'Authorization': f'Bearer {admin_token}',
        'Content-Type': 'application/json'
    }
    
    response, status = make_request(f"{BASE_URL}/auth/admin-only", "GET", headers=admin_headers)
    print(f"Status: {status}")
    print(f"Response: {response}")
    
    if status == 200:
        print("✅ Admin-only endpoint access successful")
    else:
        print("❌ Admin-only endpoint access failed")
    
    # Step 8: Test non-admin access to admin endpoint
    print("\n8. Testing non-admin access to admin endpoint...")
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    response, status = make_request(f"{BASE_URL}/auth/admin-only", "GET", headers=headers)
    print(f"Status: {status}")
    print(f"Response: {response}")
    
    if status == 403:
        print("✅ Non-admin correctly denied access to admin endpoint")
    else:
        print("❌ Non-admin access to admin endpoint should be denied")
    
    print("\n" + "=" * 50)
    print("JWT Authentication Test Complete!")
    print("=" * 50)

if __name__ == "__main__":
    test_jwt_auth()
