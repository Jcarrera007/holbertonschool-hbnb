# 🌐 HBnB API Testing with cURL

This guide provides comprehensive cURL commands to test your HBnB Flask API endpoints.

## 🚀 Prerequisites

1. **Start the Flask application:**
   ```bash
   # In WSL/Linux terminal
   cd /mnt/d/myschoolworkandGithub/holbertonschool-hbnb/part2/hbnb
   source ../../hbnb-venv/bin/activate
   python run.py
   ```

2. **Verify the server is running:**
   ```bash
   curl http://localhost:5000/api/v1/
   ```

## 📖 API Documentation

- **Swagger UI**: http://localhost:5000/api/v1/
- **Base URL**: http://localhost:5000
- **API Version**: v1

---

## 👥 User API Testing

### 1. **GET /users** - List All Users
```bash
curl -X GET http://localhost:5000/users \
  -H "Content-Type: application/json"
```

### 2. **POST /users** - Create a New User
```bash
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "is_admin": false
  }'
```

### 3. **POST /users** - Create an Admin User
```bash
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Admin",
    "last_name": "User",
    "email": "admin@hbnb.com",
    "is_admin": true
  }'
```

### 4. **GET /users/{user_id}** - Get Specific User
```bash
# Replace {USER_ID} with actual user ID from previous response
curl -X GET http://localhost:5000/users/{USER_ID} \
  -H "Content-Type: application/json"
```

### 5. **PUT /users/{user_id}** - Update User
```bash
curl -X PUT http://localhost:5000/users/{USER_ID} \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Johnny",
    "last_name": "Smith",
    "email": "johnny.smith@example.com"
  }'
```

### 6. **DELETE /users/{user_id}** - Delete User
```bash
curl -X DELETE http://localhost:5000/users/{USER_ID} \
  -H "Content-Type: application/json"
```

---

## 🏨 Amenity API Testing

### 1. **GET /amenities** - List All Amenities
```bash
curl -X GET http://localhost:5000/amenities \
  -H "Content-Type: application/json"
```

### 2. **POST /amenities** - Create a New Amenity
```bash
curl -X POST http://localhost:5000/amenities \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Wi-Fi"
  }'
```

### 3. **POST /amenities** - Create Multiple Amenities
```bash
# Create Wi-Fi
curl -X POST http://localhost:5000/amenities \
  -H "Content-Type: application/json" \
  -d '{"name": "Wi-Fi"}'

# Create Parking
curl -X POST http://localhost:5000/amenities \
  -H "Content-Type: application/json" \
  -d '{"name": "Free Parking"}'

# Create Pool
curl -X POST http://localhost:5000/amenities \
  -H "Content-Type: application/json" \
  -d '{"name": "Swimming Pool"}'
```

### 4. **GET /amenities/{amenity_id}** - Get Specific Amenity
```bash
curl -X GET http://localhost:5000/amenities/{AMENITY_ID} \
  -H "Content-Type: application/json"
```

### 5. **PUT /amenities/{amenity_id}** - Update Amenity
```bash
curl -X PUT http://localhost:5000/amenities/{AMENITY_ID} \
  -H "Content-Type: application/json" \
  -d '{
    "name": "High-Speed Wi-Fi"
  }'
```

### 6. **DELETE /amenities/{amenity_id}** - Delete Amenity
```bash
curl -X DELETE http://localhost:5000/amenities/{AMENITY_ID} \
  -H "Content-Type: application/json"
```

---

## 🧪 Complete Testing Workflow

### Step 1: Create Test Data
```bash
# Create users
USER1=$(curl -s -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Alice",
    "last_name": "Johnson",
    "email": "alice@example.com"
  }' | grep -o '"id":"[^"]*"' | cut -d'"' -f4)

USER2=$(curl -s -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Bob",
    "last_name": "Smith",
    "email": "bob@example.com"
  }' | grep -o '"id":"[^"]*"' | cut -d'"' -f4)

echo "Created users: $USER1, $USER2"

# Create amenities
WIFI=$(curl -s -X POST http://localhost:5000/amenities \
  -H "Content-Type: application/json" \
  -d '{"name": "Wi-Fi"}' | grep -o '"id":"[^"]*"' | cut -d'"' -f4)

PARKING=$(curl -s -X POST http://localhost:5000/amenities \
  -H "Content-Type: application/json" \
  -d '{"name": "Parking"}' | grep -o '"id":"[^"]*"' | cut -d'"' -f4)

echo "Created amenities: $WIFI, $PARKING"
```

### Step 2: Test All Operations
```bash
# List all users
echo "=== All Users ==="
curl -s http://localhost:5000/users | jq '.'

# List all amenities  
echo "=== All Amenities ==="
curl -s http://localhost:5000/amenities | jq '.'

# Get specific user
echo "=== User Details ==="
curl -s http://localhost:5000/users/$USER1 | jq '.'

# Update user
echo "=== Updated User ==="
curl -s -X PUT http://localhost:5000/users/$USER1 \
  -H "Content-Type: application/json" \
  -d '{"first_name": "Alice Updated"}' | jq '.'
```

---

## ❌ Error Testing

### Test Validation Errors
```bash
# Invalid email format
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Test",
    "last_name": "User",
    "email": "invalid-email"
  }'

# Missing required fields
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Test"
  }'

# Empty amenity name
curl -X POST http://localhost:5000/amenities \
  -H "Content-Type: application/json" \
  -d '{
    "name": ""
  }'
```

### Test 404 Errors
```bash
# Non-existent user
curl -X GET http://localhost:5000/users/non-existent-id

# Non-existent amenity
curl -X GET http://localhost:5000/amenities/non-existent-id
```

---

## 📊 Response Format Examples

### Successful User Creation (201)
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "first_name": "John",
  "last_name": "Doe", 
  "email": "john.doe@example.com",
  "is_admin": false,
  "created_at": "2025-06-22T10:30:00",
  "updated_at": "2025-06-22T10:30:00"
}
```

### Error Response (400)
```json
{
  "message": "Email must be in a valid format"
}
```

### Not Found Response (404)
```json
{
  "message": "User not found"
}
```

---

## 🛠️ Advanced Testing

### Using jq for JSON Processing
```bash
# Pretty print JSON responses
curl -s http://localhost:5000/users | jq '.'

# Extract specific fields
curl -s http://localhost:5000/users | jq '.[0].email'

# Count results
curl -s http://localhost:5000/users | jq 'length'
```

### Save Response to Variable
```bash
# Save user ID for later use
USER_ID=$(curl -s -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Test","last_name":"User","email":"test@example.com"}' \
  | jq -r '.id')

echo "Created user with ID: $USER_ID"

# Use the saved ID
curl -s http://localhost:5000/users/$USER_ID | jq '.'
```

### Batch Testing Script
```bash
#!/bin/bash
# Save as test_api.sh and make executable: chmod +x test_api.sh

echo "🧪 Testing HBnB API..."

# Test user creation
echo "Creating users..."
for i in {1..3}; do
  curl -s -X POST http://localhost:5000/users \
    -H "Content-Type: application/json" \
    -d "{
      \"first_name\": \"User$i\",
      \"last_name\": \"Test\",
      \"email\": \"user$i@example.com\"
    }" | jq '.id'
done

# Test amenity creation
echo "Creating amenities..."
for amenity in "Wi-Fi" "Parking" "Pool" "Gym"; do
  curl -s -X POST http://localhost:5000/amenities \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"$amenity\"}" | jq '.id'
done

echo "✅ API testing complete!"
```

---

## 🔧 Troubleshooting

### Common Issues

1. **Connection Refused**
   - Ensure Flask app is running: `python run.py`
   - Check correct port: http://localhost:5000

2. **404 Not Found**
   - Verify endpoint URL
   - Check if namespaces are registered correctly

3. **500 Internal Server Error**
   - Check Flask logs in terminal
   - Verify model imports are working

4. **JSON Parse Errors**
   - Ensure Content-Type header is set
   - Validate JSON syntax with `jq`

### Debug Commands
```bash
# Check if server is running
curl -I http://localhost:5000/

# Test basic connectivity
curl -v http://localhost:5000/api/v1/

# Check server logs
# Look at your Flask terminal for error messages
```

---

## 🎯 Next Steps

Once you've tested these endpoints successfully:

1. **Add Place API endpoints** for property management
2. **Add Review API endpoints** for user reviews  
3. **Implement relationships** between entities
4. **Add authentication** and authorization
5. **Implement pagination** for large datasets

Happy testing! 🚀
