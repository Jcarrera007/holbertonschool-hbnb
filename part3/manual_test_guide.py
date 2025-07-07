#!/usr/bin/env python3
"""
Quick Manual Test for Authenticated Endpoints

This script provides step-by-step instructions to manually test the authenticated endpoints.
"""

def print_manual_test_instructions():
    """Print manual test instructions"""
    print("=" * 70)
    print("  AUTHENTICATED ENDPOINTS MANUAL TEST")
    print("=" * 70)
    
    print("\n📋 Step 1: Create a test user")
    print('curl -X POST "http://127.0.0.1:5000/api/v1/users/" \\')
    print('  -H "Content-Type: application/json" \\')
    print('  -d \'{"first_name": "John", "last_name": "Doe", "email": "john@test.com", "password": "pass123"}\'')
    
    print("\n📋 Step 2: Create an owner user")
    print('curl -X POST "http://127.0.0.1:5000/api/v1/users/" \\')
    print('  -H "Content-Type: application/json" \\')
    print('  -d \'{"first_name": "Alice", "last_name": "Smith", "email": "alice@test.com", "password": "owner123"}\'')
    
    print("\n🔐 Step 3: Login as regular user")
    print('curl -X POST "http://127.0.0.1:5000/api/v1/auth/login" \\')
    print('  -H "Content-Type: application/json" \\')
    print('  -d \'{"email": "john@test.com", "password": "pass123"}\'')
    print("# Save the access_token from the response")
    
    print("\n🔐 Step 4: Login as owner")
    print('curl -X POST "http://127.0.0.1:5000/api/v1/auth/login" \\')
    print('  -H "Content-Type: application/json" \\')
    print('  -d \'{"email": "alice@test.com", "password": "owner123"}\'')
    print("# Save the access_token from the response")
    
    print("\n✅ Step 5: Test user update (should work - own data)")
    print('curl -X PUT "http://127.0.0.1:5000/api/v1/users/USER_ID" \\')
    print('  -H "Authorization: Bearer USER_TOKEN" \\')
    print('  -H "Content-Type: application/json" \\')
    print('  -d \'{"first_name": "Johnny"}\'')
    print("# Replace USER_ID and USER_TOKEN with actual values")
    
    print("\n❌ Step 6: Test unauthorized user update (should fail)")
    print('curl -X PUT "http://127.0.0.1:5000/api/v1/users/OWNER_ID" \\')
    print('  -H "Authorization: Bearer USER_TOKEN" \\')
    print('  -H "Content-Type: application/json" \\')
    print('  -d \'{"first_name": "Hacker"}\'')
    print("# Should return 403 Forbidden")
    
    print("\n❌ Step 7: Test email modification (should fail)")
    print('curl -X PUT "http://127.0.0.1:5000/api/v1/users/USER_ID" \\')
    print('  -H "Authorization: Bearer USER_TOKEN" \\')
    print('  -H "Content-Type: application/json" \\')
    print('  -d \'{"email": "newemail@test.com"}\'')
    print("# Should return 400 Bad Request")
    
    print("\n🏠 Step 8: Create a place (as owner)")
    print('curl -X POST "http://127.0.0.1:5000/api/v1/places/" \\')
    print('  -H "Authorization: Bearer OWNER_TOKEN" \\')
    print('  -H "Content-Type: application/json" \\')
    print('  -d \'{"title": "Cozy Apartment", "description": "Great place", "price": 120, "latitude": 37.7749, "longitude": -122.4194}\'')
    print("# Save the place ID from the response")
    
    print("\n🌐 Step 9: Test public place access (no auth needed)")
    print('curl -X GET "http://127.0.0.1:5000/api/v1/places/"')
    print('curl -X GET "http://127.0.0.1:5000/api/v1/places/PLACE_ID"')
    
    print("\n✅ Step 10: Update place (as owner - should work)")
    print('curl -X PUT "http://127.0.0.1:5000/api/v1/places/PLACE_ID" \\')
    print('  -H "Authorization: Bearer OWNER_TOKEN" \\')
    print('  -H "Content-Type: application/json" \\')
    print('  -d \'{"title": "Updated Apartment", "price": 150}\'')
    
    print("\n❌ Step 11: Update place (as non-owner - should fail)")
    print('curl -X PUT "http://127.0.0.1:5000/api/v1/places/PLACE_ID" \\')
    print('  -H "Authorization: Bearer USER_TOKEN" \\')
    print('  -H "Content-Type: application/json" \\')
    print('  -d \'{"title": "Hacked Place"}\'')
    print("# Should return 403 Forbidden")
    
    print("\n⭐ Step 12: Create review (as user - should work)")
    print('curl -X POST "http://127.0.0.1:5000/api/v1/reviews/" \\')
    print('  -H "Authorization: Bearer USER_TOKEN" \\')
    print('  -H "Content-Type: application/json" \\')
    print('  -d \'{"text": "Great place to stay!", "rating": 5, "place_id": "PLACE_ID"}\'')
    print("# Save the review ID from the response")
    
    print("\n❌ Step 13: Owner tries to review own place (should fail)")
    print('curl -X POST "http://127.0.0.1:5000/api/v1/reviews/" \\')
    print('  -H "Authorization: Bearer OWNER_TOKEN" \\')
    print('  -H "Content-Type: application/json" \\')
    print('  -d \'{"text": "My place is great!", "rating": 5, "place_id": "PLACE_ID"}\'')
    print("# Should return 400 Bad Request")
    
    print("\n❌ Step 14: Duplicate review (should fail)")
    print('curl -X POST "http://127.0.0.1:5000/api/v1/reviews/" \\')
    print('  -H "Authorization: Bearer USER_TOKEN" \\')
    print('  -H "Content-Type: application/json" \\')
    print('  -d \'{"text": "Another review", "rating": 4, "place_id": "PLACE_ID"}\'')
    print("# Should return 400 Bad Request")
    
    print("\n✅ Step 15: Update review (as author - should work)")
    print('curl -X PUT "http://127.0.0.1:5000/api/v1/reviews/REVIEW_ID" \\')
    print('  -H "Authorization: Bearer USER_TOKEN" \\')
    print('  -H "Content-Type: application/json" \\')
    print('  -d \'{"text": "Updated review - still great!", "rating": 4}\'')
    
    print("\n❌ Step 16: Update review (as non-author - should fail)")
    print('curl -X PUT "http://127.0.0.1:5000/api/v1/reviews/REVIEW_ID" \\')
    print('  -H "Authorization: Bearer OWNER_TOKEN" \\')
    print('  -H "Content-Type: application/json" \\')
    print('  -d \'{"text": "Hacked review"}\'')
    print("# Should return 403 Forbidden")
    
    print("\n✅ Step 17: Delete review (as author - should work)")
    print('curl -X DELETE "http://127.0.0.1:5000/api/v1/reviews/REVIEW_ID" \\')
    print('  -H "Authorization: Bearer USER_TOKEN"')
    print("# Should return 204 No Content")
    
    print("\n" + "=" * 70)
    print("  TEST VALIDATION CHECKLIST")
    print("=" * 70)
    print("✅ Users can only update their own profiles")
    print("✅ Email and password modification is blocked")
    print("✅ Only place owners can update/delete places")
    print("✅ Public place access works without authentication")
    print("✅ Users cannot review their own places")
    print("✅ Duplicate reviews are prevented")
    print("✅ Only review authors can update/delete reviews")
    print("✅ Proper HTTP status codes (403, 400, 401, 204)")
    print("=" * 70)

if __name__ == "__main__":
    print_manual_test_instructions()
