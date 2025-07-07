#!/usr/bin/env python3
"""
Simple JWT Authentication Test

This script tests the JWT authentication functionality with manual curl-like requests.
"""

import time
import json

def test_manual():
    """Manual test instructions"""
    print("=" * 60)
    print("  JWT Authentication Manual Test")
    print("=" * 60)
    
    print("\n1. First, create a test user:")
    print('curl -X POST "http://127.0.0.1:5000/api/v1/users/" \\')
    print('  -H "Content-Type: application/json" \\')
    print('  -d \'{"first_name": "John", "last_name": "Doe", "email": "john.doe@test.com", "password": "securepassword123", "is_admin": false}\'')
    
    print("\n2. Then login to get a JWT token:")
    print('curl -X POST "http://127.0.0.1:5000/api/v1/auth/login" \\')
    print('  -H "Content-Type: application/json" \\')
    print('  -d \'{"email": "john.doe@test.com", "password": "securepassword123"}\'')
    
    print("\n3. Test protected endpoint (replace YOUR_JWT_TOKEN with actual token):")
    print('curl -X GET "http://127.0.0.1:5000/api/v1/auth/protected" \\')
    print('  -H "Authorization: Bearer YOUR_JWT_TOKEN"')
    
    print("\n4. Create an admin user:")
    print('curl -X POST "http://127.0.0.1:5000/api/v1/users/" \\')
    print('  -H "Content-Type: application/json" \\')
    print('  -d \'{"first_name": "Admin", "last_name": "User", "email": "admin@test.com", "password": "adminpass123", "is_admin": true}\'')
    
    print("\n5. Login as admin:")
    print('curl -X POST "http://127.0.0.1:5000/api/v1/auth/login" \\')
    print('  -H "Content-Type: application/json" \\')
    print('  -d \'{"email": "admin@test.com", "password": "adminpass123"}\'')
    
    print("\n6. Test admin-only endpoint (replace YOUR_ADMIN_JWT_TOKEN with actual admin token):")
    print('curl -X GET "http://127.0.0.1:5000/api/v1/auth/admin-only" \\')
    print('  -H "Authorization: Bearer YOUR_ADMIN_JWT_TOKEN"')
    
    print("\n" + "=" * 60)
    print("Follow the steps above to test JWT authentication manually")
    print("=" * 60)

if __name__ == "__main__":
    test_manual()
