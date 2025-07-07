#!/usr/bin/env python3
"""
Test Authenticated User Access Endpoints

This script tests the authenticated user access functionality including:
- User authentication and protected user updates
- Place creation and ownership validation
- Review creation with business logic validation
- Protection of endpoints with JWT
"""

import json
import urllib.request
import urllib.parse
import urllib.error

BASE_URL = "http://127.0.0.1:5000"

def make_request(url, method='GET', data=None, headers=None):
    """Make HTTP request using urllib"""
    if headers is None:
        headers = {'Content-Type': 'application/json'}
    
    if data:
        data = json.dumps(data).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as response:
            response_body = response.read().decode()
            if response_body:
                return json.loads(response_body), response.getcode()
            else:
                return {}, response.getcode()  # Empty response for 204, etc.
    except urllib.error.HTTPError as e:
        try:
            error_data = json.loads(e.read().decode())
            return error_data, e.code
        except:
            return {'error': str(e)}, e.code

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

def test_authenticated_endpoints():
    """Test the authenticated user access endpoints"""
    
    print_section("Authenticated User Access Test Suite")
    
    # Test data
    test_user = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@test.com",
        "password": "securepassword123",
        "is_admin": False
    }
    
    owner_user = {
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice.smith@test.com",
        "password": "ownerpass123",
        "is_admin": False
    }
    
    # Step 1: Create test users
    print("\n1. Creating test users...")
    
    response, status = make_request(f"{BASE_URL}/users/", "POST", test_user)
    if status != 201:
        print_result("Create user", False, f"Status: {status}, Response: {response}")
        return
    
    user_id = response.get('id')
    print_result("Create test user", True, f"User ID: {user_id}")
    
    response, status = make_request(f"{BASE_URL}/users/", "POST", owner_user)
    if status != 201:
        print_result("Create owner", False, f"Status: {status}, Response: {response}")
        return
    
    owner_id = response.get('id')
    print_result("Create owner user", True, f"Owner ID: {owner_id}")
    
    # Step 2: Login as regular user
    print("\n2. Testing user login...")
    login_data = {
        "email": "john.doe@test.com",
        "password": "securepassword123"
    }
    
    response, status = make_request(f"{BASE_URL}/auth/login", "POST", login_data)
    if status != 200:
        print_result("User login", False, f"Status: {status}, Response: {response}")
        return
    
    user_token = response.get('access_token')
    print_result("User login", True, f"Token received")
    
    # Step 3: Login as owner
    print("\n3. Testing owner login...")
    owner_login = {
        "email": "alice.smith@test.com",
        "password": "ownerpass123"
    }
    
    response, status = make_request(f"{BASE_URL}/auth/login", "POST", owner_login)
    if status != 200:
        print_result("Owner login", False, f"Status: {status}, Response: {response}")
        return
    
    owner_token = response.get('access_token')
    print_result("Owner login", True, f"Token received")
    
    # Step 4: Test authenticated user update (own data)
    print("\n4. Testing authenticated user update...")
    update_data = {
        "first_name": "Johnny",
        "last_name": "Updated"
    }
    
    headers = {
        'Authorization': f'Bearer {user_token}',
        'Content-Type': 'application/json'
    }
    
    response, status = make_request(f"{BASE_URL}/users/{user_id}", "PUT", update_data, headers)
    print_result("Update own user data", status == 200, f"Status: {status}, Response: {response}")
    
    # Step 5: Test unauthorized user update (other user's data)
    print("\n5. Testing unauthorized user update...")
    response, status = make_request(f"{BASE_URL}/users/{owner_id}", "PUT", update_data, headers)
    print_result("Unauthorized user update blocked", status == 403, f"Status: {status}")
    
    # Step 6: Test email/password modification blocked
    print("\n6. Testing email/password modification blocked...")
    forbidden_data = {
        "email": "newemail@test.com",
        "password": "newpass"
    }
    
    response, status = make_request(f"{BASE_URL}/users/{user_id}", "PUT", forbidden_data, headers)
    print_result("Email/password modification blocked", status == 400, f"Status: {status}")
    
    # Step 7: Create a place as owner
    print("\n7. Testing authenticated place creation...")
    place_data = {
        "title": "Cozy Apartment",
        "description": "A comfortable place to stay",
        "price": 120.00,
        "latitude": 37.7749,
        "longitude": -122.4194
    }
    
    owner_headers = {
        'Authorization': f'Bearer {owner_token}',
        'Content-Type': 'application/json'
    }
    
    response, status = make_request(f"{BASE_URL}/places/", "POST", place_data, owner_headers)
    if status != 201:
        print_result("Create place", False, f"Status: {status}, Response: {response}")
        return
    
    place_id = response.get('id')
    print_result("Create place", True, f"Place ID: {place_id}")
    
    # Step 8: Test public place access
    print("\n8. Testing public place access...")
    response, status = make_request(f"{BASE_URL}/places/")
    print_result("Public places list", status == 200, f"Status: {status}")
    
    response, status = make_request(f"{BASE_URL}/places/{place_id}")
    print_result("Public place details", status == 200, f"Status: {status}")
    
    # Step 9: Test authenticated place update (by owner)
    print("\n9. Testing authenticated place update...")
    place_update = {
        "title": "Updated Apartment",
        "price": 150.00
    }
    
    response, status = make_request(f"{BASE_URL}/places/{place_id}", "PUT", place_update, owner_headers)
    print_result("Owner place update", status == 200, f"Status: {status}")
    
    # Step 10: Test unauthorized place update (by non-owner)
    print("\n10. Testing unauthorized place update...")
    response, status = make_request(f"{BASE_URL}/places/{place_id}", "PUT", place_update, headers)
    print_result("Non-owner place update blocked", status == 403, f"Status: {status}")
    
    # Step 11: Test review creation (user reviews owner's place)
    print("\n11. Testing review creation...")
    review_data = {
        "text": "Great place to stay!",
        "rating": 5,
        "place_id": place_id
    }
    
    response, status = make_request(f"{BASE_URL}/reviews/", "POST", review_data, headers)
    if status != 201:
        print_result("Create review", False, f"Status: {status}, Response: {response}")
        return
    
    review_id = response.get('id')
    print_result("Create review", True, f"Review ID: {review_id}")
    
    # Step 12: Test owner trying to review own place
    print("\n12. Testing owner reviewing own place...")
    response, status = make_request(f"{BASE_URL}/reviews/", "POST", review_data, owner_headers)
    print_result("Owner self-review blocked", status == 400, f"Status: {status}")
    
    # Step 13: Test duplicate review
    print("\n13. Testing duplicate review...")
    response, status = make_request(f"{BASE_URL}/reviews/", "POST", review_data, headers)
    print_result("Duplicate review blocked", status == 400, f"Status: {status}")
    
    # Step 14: Test review update (by author)
    print("\n14. Testing review update...")
    review_update = {
        "text": "Updated review - still great!",
        "rating": 4
    }
    
    response, status = make_request(f"{BASE_URL}/reviews/{review_id}", "PUT", review_update, headers)
    print_result("Author review update", status == 200, f"Status: {status}")
    
    # Step 15: Test unauthorized review update
    print("\n15. Testing unauthorized review update...")
    response, status = make_request(f"{BASE_URL}/reviews/{review_id}", "PUT", review_update, owner_headers)
    print_result("Unauthorized review update blocked", status == 403, f"Status: {status}")
    
    # Step 16: Test review deletion (by author)
    print("\n16. Testing review deletion...")
    response, status = make_request(f"{BASE_URL}/reviews/{review_id}", "DELETE", headers=headers)
    print_result("Author review deletion", status == 204, f"Status: {status}")
    
    print("\n" + "=" * 60)
    print("Authenticated User Access Test Complete!")
    print("=" * 60)

if __name__ == "__main__":
    test_authenticated_endpoints()
