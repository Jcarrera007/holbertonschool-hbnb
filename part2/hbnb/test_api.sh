#!/bin/bash
# HBnB API Testing Script with cURL
# Make executable with: chmod +x test_api.sh

echo "🧪 HBnB API Testing with cURL"
echo "================================"

# Check if server is running
echo "📡 Checking if server is running..."
if curl -s http://localhost:5000/api/v1/ > /dev/null; then
    echo "✅ Server is running"
else
    echo "❌ Server is not running. Please start with: python run.py"
    exit 1
fi

echo ""
echo "📝 Testing User API Endpoints..."
echo "--------------------------------"

# Test 1: Create a user
echo "1. Creating a user..."
USER_RESPONSE=$(curl -s -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "is_admin": false
  }')

echo "Response: $USER_RESPONSE"

# Extract user ID (requires jq, or we'll use grep)
if command -v jq &> /dev/null; then
    USER_ID=$(echo $USER_RESPONSE | jq -r '.id')
else
    USER_ID=$(echo $USER_RESPONSE | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
fi

echo "Created user with ID: $USER_ID"

echo ""
echo "2. Getting all users..."
curl -s -X GET http://localhost:5000/users \
  -H "Content-Type: application/json"

echo ""
echo ""
echo "3. Getting specific user..."
curl -s -X GET http://localhost:5000/users/$USER_ID \
  -H "Content-Type: application/json"

echo ""
echo ""
echo "4. Updating user..."
curl -s -X PUT http://localhost:5000/users/$USER_ID \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Johnny",
    "last_name": "Smith"
  }'

echo ""
echo ""
echo "🏨 Testing Amenity API Endpoints..."
echo "-----------------------------------"

# Test amenities
echo "1. Creating amenities..."
WIFI_RESPONSE=$(curl -s -X POST http://localhost:5000/amenities \
  -H "Content-Type: application/json" \
  -d '{"name": "Wi-Fi"}')

echo "Wi-Fi Response: $WIFI_RESPONSE"

PARKING_RESPONSE=$(curl -s -X POST http://localhost:5000/amenities \
  -H "Content-Type: application/json" \
  -d '{"name": "Free Parking"}')

echo "Parking Response: $PARKING_RESPONSE"

echo ""
echo "2. Getting all amenities..."
curl -s -X GET http://localhost:5000/amenities \
  -H "Content-Type: application/json"

echo ""
echo ""
echo "❌ Testing Error Cases..."
echo "-------------------------"

echo "1. Invalid email format:"
curl -s -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Test",
    "last_name": "User",
    "email": "invalid-email"
  }'

echo ""
echo ""
echo "2. Missing required fields:"
curl -s -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Test"
  }'

echo ""
echo ""
echo "3. Non-existent user:"
curl -s -X GET http://localhost:5000/users/non-existent-id

echo ""
echo ""
echo "🎉 API Testing Complete!"
echo "========================"
echo "✅ Check the responses above for success/error codes"
echo "📖 For more detailed testing, see: CURL_TESTING_GUIDE.md"
