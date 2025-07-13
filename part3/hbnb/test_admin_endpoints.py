#!/usr/bin/env python3
"""
Test script for admin endpoint functionality.
Tests admin-only operations across all endpoints.
"""

import requests
import json

BASE_URL = "http://localhost:5000/api/v1"

def test_admin_endpoints():
    """Test admin-only endpoint functionality."""
    
    print("=== TESTING ADMIN ENDPOINTS ===\n")
    
    # Step 1: Create admin user (should work without authentication for testing)
    print("1. Creating admin user...")
    admin_data = {
        "first_name": "Admin",
        "last_name": "User", 
        "email": "admin@test.com",
        "password": "adminpass123",
        "is_admin": True
    }
    
    try:
        response = requests.post(f"{BASE_URL}/users/", json=admin_data)
        print(f"Admin user creation: {response.status_code}")
        if response.status_code != 201:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error creating admin user: {e}")
        return
    
    # Step 2: Create regular user
    print("\n2. Creating regular user...")
    user_data = {
        "first_name": "Regular",
        "last_name": "User",
        "email": "user@test.com", 
        "password": "userpass123",
        "is_admin": False
    }
    
    try:
        response = requests.post(f"{BASE_URL}/users/", json=user_data)
        print(f"Regular user creation: {response.status_code}")
        if response.status_code != 201:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error creating regular user: {e}")
        return
    
    # Step 3: Login as admin
    print("\n3. Logging in as admin...")
    admin_login = {
        "email": "admin@test.com",
        "password": "adminpass123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=admin_login)
        print(f"Admin login: {response.status_code}")
        if response.status_code == 200:
            admin_token = response.json().get('access_token')
            print("Admin token obtained successfully")
        else:
            print(f"Admin login failed: {response.text}")
            return
    except Exception as e:
        print(f"Error logging in as admin: {e}")
        return
    
    # Step 4: Login as regular user
    print("\n4. Logging in as regular user...")
    user_login = {
        "email": "user@test.com",
        "password": "userpass123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=user_login)
        print(f"User login: {response.status_code}")
        if response.status_code == 200:
            user_token = response.json().get('access_token')
            print("User token obtained successfully")
        else:
            print(f"User login failed: {response.text}")
            return
    except Exception as e:
        print(f"Error logging in as user: {e}")
        return
    
    # Step 5: Test amenity operations
    print("\n5. Testing amenity operations...")
    
    # Admin creates amenity (should work)
    print("5a. Admin creating amenity...")
    amenity_data = {"name": "WiFi"}
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    try:
        response = requests.post(f"{BASE_URL}/amenities/", json=amenity_data, headers=headers)
        print(f"Admin amenity creation: {response.status_code}")
        if response.status_code == 201:
            amenity = response.json()
            amenity_id = amenity['id']
            print(f"Amenity created with ID: {amenity_id}")
        else:
            print(f"Failed: {response.text}")
            return
    except Exception as e:
        print(f"Error: {e}")
        return
    
    # Regular user tries to create amenity (should fail)
    print("\n5b. Regular user trying to create amenity...")
    headers = {"Authorization": f"Bearer {user_token}"}
    
    try:
        response = requests.post(f"{BASE_URL}/amenities/", json={"name": "Pool"}, headers=headers)
        print(f"User amenity creation: {response.status_code}")
        if response.status_code == 403:
            print("✓ Correctly blocked regular user from creating amenity")
        else:
            print(f"Unexpected response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Admin updates amenity (should work)
    print("\n5c. Admin updating amenity...")
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    try:
        response = requests.put(f"{BASE_URL}/amenities/{amenity_id}", 
                               json={"name": "High-Speed WiFi"}, headers=headers)
        print(f"Admin amenity update: {response.status_code}")
        if response.status_code == 200:
            print("✓ Admin successfully updated amenity")
        else:
            print(f"Failed: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Regular user tries to update amenity (should fail)
    print("\n5d. Regular user trying to update amenity...")
    headers = {"Authorization": f"Bearer {user_token}"}
    
    try:
        response = requests.put(f"{BASE_URL}/amenities/{amenity_id}", 
                               json={"name": "Free WiFi"}, headers=headers)
        print(f"User amenity update: {response.status_code}")
        if response.status_code == 403:
            print("✓ Correctly blocked regular user from updating amenity")
        else:
            print(f"Unexpected response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Regular user tries to delete amenity (should fail)
    print("\n5e. Regular user trying to delete amenity...")
    headers = {"Authorization": f"Bearer {user_token}"}
    
    try:
        response = requests.delete(f"{BASE_URL}/amenities/{amenity_id}", headers=headers)
        print(f"User amenity deletion: {response.status_code}")
        if response.status_code == 403:
            print("✓ Correctly blocked regular user from deleting amenity")
        else:
            print(f"Unexpected response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n=== ADMIN ENDPOINT TESTS COMPLETED ===")


if __name__ == "__main__":
    test_admin_endpoints()
