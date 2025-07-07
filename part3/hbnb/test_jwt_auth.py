#!/usr/bin/env python3
"""
JWT Authentication Test Script

This script tests the JWT authentication functionality including:
- User creation with password
- User login and JWT token generation
- Protected endpoint access with JWT
- Admin-only endpoint access
"""

import sys
import os
import requests
import json
import time

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

BASE_URL = "http://127.0.0.1:5000/api/v1"

def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def print_result(test_name, success, details=""):
    """Print test result with formatting"""
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status} {test_name}")
    if details:
        print(f"    {details}")

def test_jwt_authentication():
    """Test the complete JWT authentication flow"""
    
    print_section("JWT Authentication Test Suite")
    
    # Test data
    test_user = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@test.com",
        "password": "securepassword123",
        "is_admin": False
    }
    
    admin_user = {
        "first_name": "Admin",
        "last_name": "User",
        "email": "admin@test.com",
        "password": "adminpassword123",
        "is_admin": True
    }
    
    # Test 1: Create a regular user
    print_section("Test 1: User Creation")
    try:
        response = requests.post(f"{BASE_URL}/users/", json=test_user)
        if response.status_code == 201:
            user_data = response.json()
            print_result("Create regular user", True, f"User ID: {user_data['id']}")
        else:
            print_result("Create regular user", False, f"Status: {response.status_code}, Response: {response.text}")
            return
    except Exception as e:
        print_result("Create regular user", False, f"Error: {str(e)}")
        return
    
    # Test 2: Create an admin user
    print_section("Test 2: Admin Creation")
    try:
        response = requests.post(f"{BASE_URL}/users/", json=admin_user)
        if response.status_code == 201:
            admin_data = response.json()
            print_result("Create admin user", True, f"Admin ID: {admin_data['id']}")
        else:
            print_result("Create admin user", False, f"Status: {response.status_code}, Response: {response.text}")
            return
    except Exception as e:
        print_result("Create admin user", False, f"Error: {str(e)}")
        return
    
    # Test 3: Login with regular user
    print_section("Test 3: User Login")
    try:
        login_data = {
            "email": test_user["email"],
            "password": test_user["password"]
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            token_response = response.json()
            user_token = token_response["access_token"]
            print_result("User login", True, "JWT token received")
            print(f"    Token: {user_token[:50]}...")
        else:
            print_result("User login", False, f"Status: {response.status_code}, Response: {response.text}")
            return
    except Exception as e:
        print_result("User login", False, f"Error: {str(e)}")
        return
    
    # Test 4: Login with admin user
    print_section("Test 4: Admin Login")
    try:
        admin_login_data = {
            "email": admin_user["email"],
            "password": admin_user["password"]
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=admin_login_data)
        if response.status_code == 200:
            admin_token_response = response.json()
            admin_token = admin_token_response["access_token"]
            print_result("Admin login", True, "JWT token received")
            print(f"    Token: {admin_token[:50]}...")
        else:
            print_result("Admin login", False, f"Status: {response.status_code}, Response: {response.text}")
            return
    except Exception as e:
        print_result("Admin login", False, f"Error: {str(e)}")
        return
    
    # Test 5: Access protected endpoint with user token
    print_section("Test 5: Protected Endpoint Access")
    try:
        headers = {"Authorization": f"Bearer {user_token}"}
        response = requests.get(f"{BASE_URL}/auth/protected", headers=headers)
        if response.status_code == 200:
            protected_data = response.json()
            print_result("Access protected endpoint", True, f"Message: {protected_data['message']}")
        else:
            print_result("Access protected endpoint", False, f"Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print_result("Access protected endpoint", False, f"Error: {str(e)}")
    
    # Test 6: Access protected endpoint without token (should fail)
    print_section("Test 6: Unauthorized Access")
    try:
        response = requests.get(f"{BASE_URL}/auth/protected")
        if response.status_code == 401:
            print_result("Unauthorized access blocked", True, "Access correctly denied")
        else:
            print_result("Unauthorized access blocked", False, f"Status: {response.status_code} (should be 401)")
    except Exception as e:
        print_result("Unauthorized access blocked", False, f"Error: {str(e)}")
    
    # Test 7: Access admin endpoint with user token (should fail)
    print_section("Test 7: Admin Access with User Token")
    try:
        headers = {"Authorization": f"Bearer {user_token}"}
        response = requests.get(f"{BASE_URL}/auth/admin-only", headers=headers)
        if response.status_code == 403:
            print_result("Admin access denied for user", True, "Access correctly forbidden")
        else:
            print_result("Admin access denied for user", False, f"Status: {response.status_code} (should be 403)")
    except Exception as e:
        print_result("Admin access denied for user", False, f"Error: {str(e)}")
    
    # Test 8: Access admin endpoint with admin token (should succeed)
    print_section("Test 8: Admin Access with Admin Token")
    try:
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = requests.get(f"{BASE_URL}/auth/admin-only", headers=headers)
        if response.status_code == 200:
            admin_data = response.json()
            print_result("Admin access granted", True, f"Message: {admin_data['message']}")
        else:
            print_result("Admin access granted", False, f"Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print_result("Admin access granted", False, f"Error: {str(e)}")
    
    # Test 9: Invalid login credentials
    print_section("Test 9: Invalid Credentials")
    try:
        invalid_login = {
            "email": test_user["email"],
            "password": "wrongpassword"
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=invalid_login)
        if response.status_code == 401:
            print_result("Invalid credentials rejected", True, "Login correctly denied")
        else:
            print_result("Invalid credentials rejected", False, f"Status: {response.status_code} (should be 401)")
    except Exception as e:
        print_result("Invalid credentials rejected", False, f"Error: {str(e)}")
    
    print_section("JWT Authentication Test Complete")
    print("🎉 All JWT authentication tests completed!")

def check_server():
    """Check if the Flask server is running"""
    try:
        response = requests.get(f"{BASE_URL}/")
        return response.status_code == 200
    except:
        return False

if __name__ == "__main__":
    print("🔐 JWT Authentication Test Suite")
    print("=" * 60)
    
    # Check if server is running
    if not check_server():
        print("❌ Flask server is not running!")
        print("Please start the server with: python run.py")
        sys.exit(1)
    
    print("✅ Flask server is running")
    
    # Wait a moment to ensure server is ready
    time.sleep(1)
    
    # Run the tests
    test_jwt_authentication()
