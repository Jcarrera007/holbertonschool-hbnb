# Authenticated User Access Endpoints Implementation

## Overview
The HBnB application now implements comprehensive authenticated user access controls using JWT authentication. Users can only perform actions on resources they own, with proper validation and authorization checks.

## Implemented Security Features

### 1. JWT-Protected Endpoints

#### User Management
- **PUT /api/v1/users/<user_id>**: Users can only update their own profile
  - Authentication required via JWT token
  - User ID validation (must match token user ID)
  - Email and password modification blocked
  - Returns 403 for unauthorized access attempts

#### Place Management
- **POST /api/v1/places/**: Create new places (authenticated users only)
  - Owner automatically set to authenticated user
  - Full place data validation
  - Returns 201 with created place data

- **PUT /api/v1/places/<place_id>**: Update places (owners only)
  - Ownership validation (only place owner can update)
  - Returns 403 for non-owners
  - Full place data validation

- **DELETE /api/v1/places/<place_id>**: Delete places (owners only)
  - Ownership validation required
  - Returns 403 for non-owners
  - Returns 204 on successful deletion

#### Review Management
- **POST /api/v1/reviews/**: Create reviews (authenticated users only)
  - Business logic: Users cannot review their own places
  - Duplicate review prevention (one review per user per place)
  - Returns 400 for self-reviews or duplicates
  - Returns 201 with created review data

- **PUT /api/v1/reviews/<review_id>**: Update reviews (authors only)
  - Authorship validation (only review author can update)
  - Returns 403 for non-authors
  - Text and rating updates allowed

- **DELETE /api/v1/reviews/<review_id>**: Delete reviews (authors only)
  - Authorship validation required
  - Returns 403 for non-authors
  - Returns 204 on successful deletion

### 2. Public Endpoints (No Authentication Required)

#### Read-Only Access
- **GET /api/v1/places/**: List all places
- **GET /api/v1/places/<place_id>**: Get place details
- **GET /api/v1/reviews/**: List all reviews
- **GET /api/v1/reviews/<review_id>**: Get review details
- **GET /api/v1/reviews/places/<place_id>**: Get reviews for a place

### 3. Authorization Logic

#### Ownership Validation
```python
# Example: Place ownership check
current_user = get_jwt_identity()
if place.owner.id != current_user['id']:
    return {'error': 'Unauthorized action'}, 403
```

#### Business Rules Enforcement
```python
# Example: Prevent self-reviews
if place.owner.id == current_user['id']:
    return {'error': 'You cannot review your own place'}, 400

# Example: Prevent duplicate reviews
for review in reviews_storage.values():
    if review.user.id == current_user['id'] and review.place.id == place_id:
        return {'error': 'You have already reviewed this place'}, 400
```

#### Data Protection
```python
# Example: Prevent email/password modification
if 'email' in data or 'password' in data:
    return {'error': 'You cannot modify email or password'}, 400
```

## Error Response Standards

### HTTP Status Codes
- **400 Bad Request**: Invalid data or business rule violations
- **401 Unauthorized**: Missing or invalid JWT token
- **403 Forbidden**: Valid token but insufficient permissions
- **404 Not Found**: Resource does not exist

### Error Message Examples
```json
{"error": "Unauthorized action"}
{"error": "You cannot review your own place"}
{"error": "You have already reviewed this place"}
{"error": "You cannot modify email or password"}
```

## Testing

### Test Script
The `test_authenticated_endpoints.py` script provides comprehensive testing for:
- User authentication and token generation
- Authorized and unauthorized operations
- Business rule enforcement
- Public endpoint access
- Error handling and status codes

### Manual Testing Examples

#### Create Place (Authenticated)
```bash
curl -X POST "http://127.0.0.1:5000/api/v1/places/" \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "My Place", "description": "Great location", "price": 100, "latitude": 37.7749, "longitude": -122.4194}'
```

#### Update User (Self Only)
```bash
curl -X PUT "http://127.0.0.1:5000/api/v1/users/<your_user_id>" \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{"first_name": "Updated Name"}'
```

#### Create Review (Business Logic)
```bash
curl -X POST "http://127.0.0.1:5000/api/v1/reviews/" \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{"text": "Great stay!", "rating": 5, "place_id": "<place_id>"}'
```

## Security Benefits

### Data Integrity
- Users can only modify their own data
- Place owners control their property information
- Review authors maintain control over their content

### Business Logic Enforcement
- Prevents conflicts of interest (self-reviews)
- Ensures data consistency (one review per user per place)
- Protects sensitive user information

### Scalable Authorization
- Token-based authentication (stateless)
- Fine-grained permission controls
- Clear separation of public and private operations

## Implementation Details

### JWT Token Structure
```json
{
  "id": "user_uuid",
  "is_admin": false,
  "exp": "expiration_timestamp"
}
```

### Database Relations
- Places linked to user owners
- Reviews linked to both users and places
- Ownership tracked through foreign key relationships

### Validation Pipeline
1. JWT token validation (authentication)
2. Resource existence check
3. Ownership/authorship validation (authorization)
4. Business rule enforcement
5. Data validation and processing

This implementation provides a secure, scalable foundation for the HBnB application with proper authentication and authorization controls.
