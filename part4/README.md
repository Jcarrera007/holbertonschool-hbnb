# HBnB Frontend - Part 4

This directory contains the frontend implementation for the HBnB (Airbnb clone) project with JWT-based authentication.

## 📁 Project Structure

```
part4/
├── index.html          # Main page with list of places
├── login.html          # Login form page
├── place.html          # Place details page
├── add_review.html     # Add review form page
├── styles.css          # CSS styling
├── scripts.js          # Main JavaScript functionality
├── images/             # Image assets
│   ├── logo.png        # HBnB logo
│   ├── icon.png        # Favicon
│   ├── icon_wifi.png   # Wi-Fi amenity icon
│   ├── icon_bed.png    # Bedroom amenity icon
│   └── icon_bath.png   # Bathroom amenity icon
└── README.md           # This file
```

## ✨ Features Implemented

### 🔐 JWT Authentication
- **Login Form**: Email/password authentication with API integration
- **JWT Token Storage**: Secure token storage in HTTP-only cookies
- **Session Management**: Automatic token validation and logout
- **Protected Routes**: Authentication required for review submission

### 🏠 Place Management
- **Dynamic Place Loading**: API integration with fallback to mock data
- **Place Listings**: Grid display with title, description, location, and price
- **Place Details**: Detailed view with amenities and reviews
- **Amenity Icons**: Visual amenity indicators with provided icons
- **Guest/User Access**: Places accessible to both authenticated and unauthenticated users
- **Responsive Design**: Mobile-friendly layout

### 🔍 Filtering System
- **Price-based Filtering**: Client-side filtering without page reload
- **Filter Options**: Up to $10, $50, $100, or show all places
- **Real-time Updates**: Instant filtering results
- **No-results Handling**: Appropriate messaging when no places match criteria

### ⭐ Review System
- **View Reviews**: Display existing reviews with ratings
- **Add Reviews**: Authenticated users can submit reviews via dedicated form
- **Review Validation**: Comprehensive form validation and error handling
- **Star Ratings**: Visual star rating system (1-5 stars)
- **API Integration**: Review submission to backend with JWT authentication
- **Authentication Required**: Only logged-in users can add reviews
- **Automatic Redirect**: Unauthenticated users redirected to index page

## 🔧 Configuration

### API Configuration
Update the API base URL in `scripts.js`:

```javascript
const API_BASE_URL = 'http://localhost:5000/api/v1'; // Update this to match your API URL
```

### Expected API Endpoints

The frontend expects the following API endpoints:

#### Authentication
- **POST** `/api/v1/auth/login`
  - **Request**: `{ "email": "user@example.com", "password": "password123" }`
  - **Response**: `{ "access_token": "jwt_token_here", "user": { "id": "user_id", "email": "user@example.com" } }`

#### Places
- **GET** `/api/v1/places` - Get all places
  - **Headers**: `Authorization: Bearer {token}` (optional)
  - **Response**: Array of place objects
  - **Note**: Works with or without authentication
- **GET** `/api/v1/places/{id}` - Get place details
  - **Headers**: `Authorization: Bearer {token}` (optional)
  - **Response**: Single place object with details, amenities, and reviews
  - **Note**: Works with or without authentication

#### Reviews
- **POST** `/api/v1/places/{id}/reviews` - Add review to place
  - **Headers**: `Authorization: Bearer {token}` (required)
  - **Request**: `{ "rating": 5, "comment": "Great place!" }`
  - **Response**: Review object with confirmation
- **GET** `/api/v1/places/{id}/reviews` - Get place reviews (Future Implementation)

## 🧪 Testing Instructions

### Prerequisites
1. Ensure your HBnB API backend is running (usually on `http://localhost:5000`)
2. Have a web server running to serve the HTML files (can't open directly in browser due to CORS)

### Setting Up a Local Web Server

#### Option 1: Python HTTP Server
```bash
cd /path/to/holbertonschool-hbnb/part4
python3 -m http.server 8000
```
Then visit: `http://localhost:8000`

#### Option 2: Node.js HTTP Server
```bash
cd /path/to/holbertonschool-hbnb/part4
npx http-server -p 8000
```

#### Option 3: PHP Built-in Server
```bash
cd /path/to/holbertonschool-hbnb/part4
php -S localhost:8000
```

### Test Cases

#### 1. Login Functionality Tests

**Test 1: Valid Login**
1. Navigate to `http://localhost:8000/login.html`
2. Enter valid credentials from your backend API
3. Click "Login"
4. **Expected**: Success message, redirect to index.html, JWT token stored in cookies

**Test 2: Invalid Login**
1. Navigate to `http://localhost:8000/login.html`
2. Enter invalid credentials (wrong email/password)
3. Click "Login"
4. **Expected**: Error message displayed, no redirect

**Test 3: Empty Fields**
1. Navigate to `http://localhost:8000/login.html`
2. Leave email or password empty
3. Click "Login"
4. **Expected**: Validation error message

**Test 4: Network Error**
1. Stop your backend API server
2. Try to login
3. **Expected**: Network error message

#### 2. Authentication State Tests

**Test 5: Authenticated User Navigation**
1. Login successfully
2. Navigate between pages (index.html, place.html)
3. **Expected**: Login button shows "Logout", user-specific content visible

**Test 6: Logout Functionality**
1. While logged in, click "Logout" in header
2. **Expected**: Redirect to index.html, login button restored, JWT token removed

**Test 7: Unauthenticated Review Access**
1. Ensure you're logged out
2. Navigate to `add_review.html`
3. **Expected**: Error message, redirect to login page

#### 3. Review System Tests

**Test 8: Add Review (Authenticated)**
1. Login successfully
2. Navigate to place details page
3. Fill out review form in the page or go to add_review.html
4. Submit review
5. **Expected**: Success message, review appears in reviews list

**Test 9: Review Validation**
1. While logged in, try to submit review with:
   - Empty fields
   - Review text less than 10 characters
2. **Expected**: Appropriate validation errors

#### 4. Places Display and Filtering Tests

**Test 10: Places Loading (Unauthenticated)**
1. Clear all cookies and reload index.html
2. Observe page loading
3. **Expected**: Places load without authentication, login link visible

**Test 11: Places Loading (Authenticated)**
1. Login successfully and navigate to index.html
2. **Expected**: Places load with authentication, logout link visible instead of login

**Test 12: Price Filter - All Places**
1. Navigate to index.html
2. Ensure "All" is selected in price filter dropdown
3. **Expected**: All 6 mock places are visible

**Test 13: Price Filter - Up to $10**
1. Select "Up to $10" from price filter dropdown
2. **Expected**: No places shown (all mock places are above $10)

**Test 14: Price Filter - Up to $50**
1. Select "Up to $50" from price filter dropdown
2. **Expected**: No places shown (all mock places are above $50)

**Test 15: Price Filter - Up to $100**
1. Select "Up to $100" from price filter dropdown
2. **Expected**: 3 places shown (Mountain View Cabin $85, Urban Loft $95, Country House $75)

**Test 16: Places API Integration**
1. Start your backend API server
2. Navigate to index.html
3. Check browser console for API requests
4. **Expected**: GET request to `/api/v1/places`, fallback to mock data if API fails

**Test 17: Dynamic Place Cards**
1. Navigate to index.html
2. Inspect the generated place cards
3. **Expected**: Each card contains title, description, location, price, and "View Details" button

#### 5. Cookie Management Tests

**Test 18: Token Persistence**
1. Login successfully
2. Close browser tab
3. Reopen and navigate to the site
4. **Expected**: Still logged in (token persists in cookie)

**Test 19: Token Expiration Handling**
1. Login successfully
2. Manually delete the token cookie using browser dev tools
3. Try to reload index.html
4. **Expected**: Login link appears, places still load (guest mode)

#### 6. Place Details Tests

**Test 20: Place Details Loading (URL Parameter)**
1. Navigate to `place.html?id=1`
2. Observe page loading and content
3. **Expected**: Place details load correctly with title, description, price, location, amenities, and reviews

**Test 21: Place Details API Integration**
1. Start your backend API server
2. Navigate to `place.html?id=1`
3. Check browser console for API requests
4. **Expected**: GET request to `/api/v1/places/1`, fallback to mock data if API fails

**Test 22: Authentication-Based Review Form (Authenticated)**
1. Login successfully
2. Navigate to `place.html?id=1`
3. **Expected**: "Add Your Review" form is visible and functional

**Test 23: Authentication-Based Review Form (Unauthenticated)**
1. Ensure you're logged out (clear cookies)
2. Navigate to `place.html?id=1`
3. **Expected**: "Add Your Review" form is hidden

**Test 24: Place Details - Different Places**
1. Navigate to `place.html?id=1`, `place.html?id=2`, `place.html?id=3`
2. **Expected**: Different place information loads for each ID

**Test 25: Place Details - Invalid ID**
1. Navigate to `place.html?id=999`
2. **Expected**: Defaults to place ID 1 (mock data fallback)

**Test 26: Place Details - Missing ID**
1. Navigate to `place.html` (no ID parameter)
2. **Expected**: Error message "Place ID not found in URL"

**Test 27: Dynamic Content Loading**
1. Navigate to any place details page
2. **Expected**: Loading message appears first, then replaced with place content

#### 7. Add Review Tests

**Test 28: Add Review Authentication Check (Unauthenticated)**
1. Ensure you're logged out (clear cookies)
2. Navigate to `add_review.html?place_id=1`
3. **Expected**: Error message appears, redirect to index.html after 2 seconds

**Test 29: Add Review Authentication Check (Authenticated)**
1. Login successfully
2. Navigate to `add_review.html?place_id=1`
3. **Expected**: Review form loads with place information displayed

**Test 30: Add Review - Missing Place ID**
1. Login successfully
2. Navigate to `add_review.html` (no place_id parameter)
3. **Expected**: Error message "Place ID not found in URL", redirect to index.html

**Test 31: Add Review Form Validation - Empty Fields**
1. Login and navigate to `add_review.html?place_id=1`
2. Submit form without filling required fields
3. **Expected**: Error message "Please fill in all required fields"

**Test 32: Add Review Form Validation - Short Comment**
1. Login and navigate to `add_review.html?place_id=1`
2. Enter rating but comment less than 10 characters
3. Submit form
4. **Expected**: Error message "Review must be at least 10 characters long"

**Test 33: Add Review Form Validation - Invalid Rating**
1. Login and navigate to `add_review.html?place_id=1`
2. Try to submit with no rating selected
3. **Expected**: Error message "Please fill in all required fields"

**Test 34: Add Review API Integration**
1. Start your backend API server
2. Login and navigate to `add_review.html?place_id=1`
3. Fill out and submit valid review
4. Check browser console for API requests
5. **Expected**: POST request to `/api/v1/places/1/reviews` with JWT token

**Test 35: Add Review Success Flow**
1. Login and navigate to `add_review.html?place_id=1`
2. Fill out valid review (rating and comment)
3. Submit form
4. **Expected**: Success message, form cleared, redirect to `place.html?id=1`

**Test 36: Add Review Error Handling**
1. Stop your backend API server
2. Login and navigate to `add_review.html?place_id=1`
3. Submit valid review
4. **Expected**: Network error message displayed

**Test 37: Add Review Navigation from Place Details**
1. Login and navigate to `place.html?id=1`
2. Click "Add a Review" button
3. **Expected**: Navigate to `add_review.html?place_id=1` with correct place info

**Test 38: Add Review Loading States**
1. Login and navigate to `add_review.html?place_id=1`
2. Submit valid review
3. **Expected**: Submit button shows "Submitting..." during API call

### Debugging Tools

#### Check Cookies
1. Open browser Developer Tools (F12)
2. Go to Application/Storage tab
3. Check Cookies section for your domain
4. Look for `token`, `userEmail`, `userId` cookies

#### Check Network Requests
1. Open Developer Tools
2. Go to Network tab
3. Perform login action
4. Check the login request and response

#### Check Console Logs
1. Open Developer Tools
2. Go to Console tab
3. Look for any JavaScript errors or debug messages

## 🛠️ Customization

### Adding New API Endpoints
To add new API calls, use the `Auth.makeAuthenticatedRequest()` method:

```javascript
// Example: Fetch user places
async function getUserPlaces() {
    try {
        const response = await window.HBnB.Auth.makeAuthenticatedRequest(
            `${window.HBnB.API_BASE_URL}/users/places`
        );
        const places = await response.json();
        return places;
    } catch (error) {
        console.error('Error fetching user places:', error);
        window.HBnB.UI.showError('Failed to load your places');
    }
}
```

### Styling Customization
Modify `styles.css` to change the visual appearance. Key classes:
- `.place-card` - Place listing cards
- `.form-container` - Form styling
- `.review-card` - Review display cards
- `.amenity-tag` - Amenity display tags

### Adding New Pages
1. Create new HTML file with similar structure
2. Include `<script src="scripts.js"></script>`
3. Use `window.HBnB.Auth.isAuthenticated()` for auth checks
4. Use `window.HBnB.UI.showError()` and `window.HBnB.UI.showSuccess()` for user feedback

## 🚨 Common Issues

### Issue: CORS Errors
**Problem**: Cannot access API from file:// protocol
**Solution**: Use a local web server (see setup instructions above)

### Issue: Login Doesn't Work
**Problem**: No response from login API
**Solution**: 
1. Check that backend API is running
2. Verify API_BASE_URL in scripts.js
3. Check browser console for error messages

### Issue: Authentication Not Persisting
**Problem**: User gets logged out on page refresh
**Solution**: Check that cookies are being set correctly in browser dev tools

### Issue: Reviews Not Submitting
**Problem**: Review form doesn't work
**Solution**: Ensure user is logged in and check console for errors

## 📝 API Response Examples

### Successful Login Response
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "user-123",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

### Places List Response
```json
[
  {
    "id": "place-123",
    "title": "Cozy Downtown Apartment",
    "description": "A beautiful apartment in the heart of the city",
    "price_per_night": 120,
    "city": "New York",
    "country": "USA",
    "owner": {
      "first_name": "John",
      "last_name": "Doe"
    }
  }
]
```

### Place Details Response
```json
{
  "id": "place-123",
  "title": "Cozy Downtown Apartment",
  "description": "A beautiful apartment in the heart of the city",
  "price_per_night": 120,
  "city": "New York",
  "country": "USA",
  "owner": {
    "first_name": "John",
    "last_name": "Doe"
  },
  "amenities": [
    {
      "name": "Wi-Fi",
      "icon": "images/icon_wifi.png"
    },
    {
      "name": "2 Bedrooms",
      "icon": "images/icon_bed.png"
    }
  ],
  "reviews": [
    {
      "id": "review-456",
      "user": {
        "first_name": "Alice",
        "last_name": "Johnson"
      },
      "rating": 5,
      "comment": "Absolutely loved staying here! Perfect location."
    }
  ]
}
```

### Review Submission Response
```json
{
  "id": "review-789",
  "user": {
    "first_name": "John",
    "last_name": "Doe"
  },
  "rating": 5,
  "comment": "Great place! Highly recommended.",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Error Response
```json
{
  "message": "Invalid credentials",
  "status": "error"
}
```

## 🔒 Security Features

- **JWT Token Storage**: Tokens stored in secure HTTP-only cookies
- **Input Validation**: Client-side form validation
- **XSS Protection**: Proper HTML escaping for user content
- **Authentication Checks**: Protected routes require valid tokens
- **Token Expiration**: Automatic logout on token expiration

## 📞 Support

If you encounter issues:
1. Check the browser console for error messages
2. Verify your backend API is running and accessible
3. Ensure all required files are present in the correct structure
4. Test with a fresh browser session (clear cookies/cache)