/**
 * HBnB Frontend JavaScript
 * Handles authentication, API calls, and UI interactions
 */

// Configuration
const API_BASE_URL = 'http://localhost:5000/api/v1'; // Update this to match your API URL

// Cookie utility functions
const CookieManager = {
    /**
     * Set a cookie with name, value, and optional parameters
     */
    setCookie: function(name, value, days = 7, path = '/') {
        let expires = '';
        if (days) {
            const date = new Date();
            date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
            expires = `; expires=${date.toUTCString()}`;
        }
        document.cookie = `${name}=${value || ''}${expires}; path=${path}; SameSite=Lax`;
    },

    /**
     * Get a cookie value by name
     */
    getCookie: function(name) {
        const nameEQ = `${name}=`;
        const ca = document.cookie.split(';');
        for (let i = 0; i < ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) === ' ') c = c.substring(1, c.length);
            if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
        }
        return null;
    },

    /**
     * Delete a cookie by name
     */
    deleteCookie: function(name, path = '/') {
        document.cookie = `${name}=; Max-Age=-99999999; path=${path}`;
    }
};

// Authentication functions
const Auth = {
    /**
     * Login user with email and password
     */
    loginUser: async function(email, password) {
        try {
            const response = await fetch(`${API_BASE_URL}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 
                    email: email, 
                    password: password 
                })
            });

            const data = await response.json();

            if (response.ok) {
                // Store JWT token in cookie
                CookieManager.setCookie('token', data.access_token, 7);
                
                // Store user info if provided
                if (data.user) {
                    CookieManager.setCookie('userEmail', data.user.email, 7);
                    CookieManager.setCookie('userId', data.user.id, 7);
                }

                return { success: true, data: data };
            } else {
                return { 
                    success: false, 
                    message: data.message || 'Login failed. Please check your credentials.' 
                };
            }
        } catch (error) {
            console.error('Login error:', error);
            return { 
                success: false, 
                message: 'Network error. Please check your connection and try again.' 
            };
        }
    },

    /**
     * Logout user by clearing cookies
     */
    logout: function() {
        CookieManager.deleteCookie('token');
        CookieManager.deleteCookie('userEmail');
        CookieManager.deleteCookie('userId');
        
        // Clear localStorage as well for backward compatibility
        localStorage.removeItem('isLoggedIn');
        localStorage.removeItem('userEmail');
        
        window.location.href = 'index.html';
    },

    /**
     * Check if user is authenticated
     */
    isAuthenticated: function() {
        const token = CookieManager.getCookie('token');
        return token !== null && token !== '';
    },

    /**
     * Get current user token
     */
    getToken: function() {
        return CookieManager.getCookie('token');
    },

    /**
     * Get current user email
     */
    getUserEmail: function() {
        return CookieManager.getCookie('userEmail');
    },

    /**
     * Make authenticated API request
     */
    makeAuthenticatedRequest: async function(url, options = {}) {
        const token = this.getToken();
        
        if (!token) {
            throw new Error('No authentication token found');
        }

        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        };

        const mergedOptions = {
            ...defaultOptions,
            ...options,
            headers: {
                ...defaultOptions.headers,
                ...options.headers
            }
        };

        try {
            const response = await fetch(url, mergedOptions);
            
            if (response.status === 401) {
                // Token expired or invalid, logout user
                this.logout();
                throw new Error('Authentication expired. Please login again.');
            }
            
            return response;
        } catch (error) {
            console.error('Authenticated request error:', error);
            throw error;
        }
    }
};

// UI Helper functions
const UI = {
    /**
     * Show error message to user
     */
    showError: function(message, containerId = null) {
        // Remove existing error messages
        const existingErrors = document.querySelectorAll('.error-message');
        existingErrors.forEach(error => error.remove());

        // Create error element
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.style.cssText = `
            background-color: #f8d7da;
            color: #721c24;
            padding: 12px;
            border: 1px solid #f5c6cb;
            border-radius: 4px;
            margin-bottom: 15px;
            font-size: 14px;
        `;
        errorDiv.textContent = message;

        // Insert error message
        if (containerId) {
            const container = document.getElementById(containerId);
            if (container) {
                container.insertBefore(errorDiv, container.firstChild);
            }
        } else {
            // Insert at the top of the form or main content
            const form = document.querySelector('form');
            const main = document.querySelector('main');
            const target = form || main;
            if (target) {
                target.insertBefore(errorDiv, target.firstChild);
            }
        }

        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.remove();
            }
        }, 5000);
    },

    /**
     * Show success message to user
     */
    showSuccess: function(message, containerId = null) {
        const successDiv = document.createElement('div');
        successDiv.className = 'success-message';
        successDiv.style.cssText = `
            background-color: #d4edda;
            color: #155724;
            padding: 12px;
            border: 1px solid #c3e6cb;
            border-radius: 4px;
            margin-bottom: 15px;
            font-size: 14px;
        `;
        successDiv.textContent = message;

        if (containerId) {
            const container = document.getElementById(containerId);
            if (container) {
                container.insertBefore(successDiv, container.firstChild);
            }
        } else {
            const form = document.querySelector('form');
            const main = document.querySelector('main');
            const target = form || main;
            if (target) {
                target.insertBefore(successDiv, target.firstChild);
            }
        }

        setTimeout(() => {
            if (successDiv.parentNode) {
                successDiv.remove();
            }
        }, 3000);
    },

    /**
     * Update login/logout buttons based on authentication status
     */
    updateAuthUI: function() {
        const isAuthenticated = Auth.isAuthenticated();
        const userEmail = Auth.getUserEmail();
        
        // Update header login button
        const loginLink = document.getElementById('login-link');
        const navLogin = document.getElementById('nav-login');
        
        if (isAuthenticated) {
            if (loginLink) {
                loginLink.textContent = 'Logout';
                loginLink.href = '#';
                loginLink.onclick = function(e) {
                    e.preventDefault();
                    Auth.logout();
                };
            }
            
            if (navLogin) {
                navLogin.textContent = 'Logout';
                navLogin.href = '#';
                navLogin.onclick = function(e) {
                    e.preventDefault();
                    Auth.logout();
                };
            }

            // Show user-specific content
            const authSections = document.querySelectorAll('.auth-hidden');
            authSections.forEach(section => {
                section.classList.remove('auth-hidden');
                section.classList.add('auth-visible');
            });
        } else {
            if (loginLink) {
                loginLink.textContent = 'Login';
                loginLink.href = 'login.html';
                loginLink.onclick = null;
            }
            
            if (navLogin) {
                navLogin.textContent = 'Login';
                navLogin.href = 'login.html';
                navLogin.onclick = null;
            }

            // Hide user-specific content
            const authSections = document.querySelectorAll('.auth-visible');
            authSections.forEach(section => {
                section.classList.remove('auth-visible');
                section.classList.add('auth-hidden');
            });
        }
    }
};

// Places management
const Places = {
    allPlaces: [],
    filteredPlaces: [],

    /**
     * Fetch places from API
     */
    fetchPlaces: async function(token = null) {
        try {
            const headers = {
                'Content-Type': 'application/json'
            };

            // Include token if provided
            if (token) {
                headers['Authorization'] = `Bearer ${token}`;
            }

            const response = await fetch(`${API_BASE_URL}/places`, {
                method: 'GET',
                headers: headers
            });

            if (response.ok) {
                const places = await response.json();
                this.allPlaces = places;
                this.filteredPlaces = [...places]; // Copy for filtering
                return { success: true, data: places };
            } else {
                console.log('API request failed, using mock data');
                // Fallback to mock data if API fails
                const mockPlaces = this.getMockPlaces();
                this.allPlaces = mockPlaces;
                this.filteredPlaces = [...mockPlaces];
                return { success: true, data: mockPlaces };
            }
        } catch (error) {
            console.error('Error fetching places:', error);
            console.log('Using mock data due to error');
            // Fallback to mock data
            const mockPlaces = this.getMockPlaces();
            this.allPlaces = mockPlaces;
            this.filteredPlaces = [...mockPlaces];
            return { success: true, data: mockPlaces };
        }
    },

    /**
     * Get mock places data for development/testing
     */
    getMockPlaces: function() {
        return [
            {
                id: '1',
                title: 'Cozy Downtown Apartment',
                description: 'A beautiful apartment in the heart of the city',
                price_per_night: 120,
                city: 'New York',
                country: 'USA',
                owner: { first_name: 'John', last_name: 'Doe' }
            },
            {
                id: '2',
                title: 'Mountain View Cabin',
                description: 'Peaceful cabin with stunning mountain views',
                price_per_night: 85,
                city: 'Aspen',
                country: 'USA',
                owner: { first_name: 'Jane', last_name: 'Smith' }
            },
            {
                id: '3',
                title: 'Beachfront Villa',
                description: 'Luxurious villa with direct beach access',
                price_per_night: 200,
                city: 'Miami',
                country: 'USA',
                owner: { first_name: 'Mike', last_name: 'Johnson' }
            },
            {
                id: '4',
                title: 'Urban Loft',
                description: 'Modern loft in trendy neighborhood',
                price_per_night: 95,
                city: 'San Francisco',
                country: 'USA',
                owner: { first_name: 'Sarah', last_name: 'Wilson' }
            },
            {
                id: '5',
                title: 'Country House',
                description: 'Charming house in peaceful countryside',
                price_per_night: 75,
                city: 'Vermont',
                country: 'USA',
                owner: { first_name: 'David', last_name: 'Brown' }
            },
            {
                id: '6',
                title: 'City Center Studio',
                description: 'Compact studio in the city center',
                price_per_night: 110,
                city: 'Boston',
                country: 'USA',
                owner: { first_name: 'Lisa', last_name: 'Davis' }
            }
        ];
    },

    /**
     * Display places in the DOM
     */
    displayPlaces: function(places) {
        const placesList = document.getElementById('places-list');
        const loadingMessage = document.getElementById('loading-message');
        
        if (!placesList) return;

        // Hide loading message
        if (loadingMessage) {
            loadingMessage.style.display = 'none';
        }

        // Clear current content
        placesList.innerHTML = '';

        if (!places || places.length === 0) {
            placesList.innerHTML = '<div class="loading">No places found matching your criteria.</div>';
            return;
        }

        // Create place cards
        places.forEach(place => {
            const placeCard = document.createElement('div');
            placeCard.className = 'place-card';
            placeCard.dataset.price = place.price_per_night;

            placeCard.innerHTML = `
                <div class="placeholder-image">${place.title}</div>
                <h3>${place.title}</h3>
                <p class="place-description">${place.description}</p>
                <p class="place-location">${place.city}, ${place.country}</p>
                <p class="price">$${place.price_per_night} per night</p>
                <a href="place.html?id=${place.id}" class="details-button">View Details</a>
            `;

            placesList.appendChild(placeCard);
        });
    },

    /**
     * Filter places by price
     */
    filterPlacesByPrice: function(maxPrice) {
        if (maxPrice === 'all') {
            this.filteredPlaces = [...this.allPlaces];
        } else {
            this.filteredPlaces = this.allPlaces.filter(place => 
                place.price_per_night <= parseInt(maxPrice)
            );
        }
        this.displayPlaces(this.filteredPlaces);
    }
};

// Authentication UI management
const AuthUI = {
    /**
     * Check authentication and control login link visibility
     */
    checkAuthentication: function() {
        const token = CookieManager.getCookie('token');
        const loginLink = document.getElementById('login-link');
        
        if (!token) {
            // User not authenticated - show login link
            if (loginLink) {
                loginLink.style.display = 'block';
                loginLink.textContent = 'Login';
                loginLink.href = 'login.html';
                loginLink.onclick = null;
            }
            
            // Load places without authentication
            this.loadPlacesForGuest();
        } else {
            // User authenticated - hide login link, show logout
            if (loginLink) {
                loginLink.style.display = 'block';
                loginLink.textContent = 'Logout';
                loginLink.href = '#';
                loginLink.onclick = function(e) {
                    e.preventDefault();
                    Auth.logout();
                };
            }
            
            // Load places with authentication
            this.loadPlacesForUser(token);
        }
        
        // Update nav login link as well
        this.updateNavAuthLinks(!!token);
    },

    /**
     * Update navigation authentication links
     */
    updateNavAuthLinks: function(isAuthenticated) {
        const navLogin = document.getElementById('nav-login');
        
        if (navLogin) {
            if (isAuthenticated) {
                navLogin.textContent = 'Logout';
                navLogin.href = '#';
                navLogin.onclick = function(e) {
                    e.preventDefault();
                    Auth.logout();
                };
            } else {
                navLogin.textContent = 'Login';
                navLogin.href = 'login.html';
                navLogin.onclick = null;
            }
        }
    },

    /**
     * Load places for authenticated user
     */
    loadPlacesForUser: async function(token) {
        try {
            const result = await Places.fetchPlaces(token);
            if (result.success) {
                Places.displayPlaces(result.data);
                this.setupPriceFilter();
            }
        } catch (error) {
            console.error('Error loading places for user:', error);
            UI.showError('Failed to load places. Please try again.');
        }
    },

    /**
     * Load places for guest user (no authentication)
     */
    loadPlacesForGuest: async function() {
        try {
            const result = await Places.fetchPlaces();
            if (result.success) {
                Places.displayPlaces(result.data);
                this.setupPriceFilter();
            }
        } catch (error) {
            console.error('Error loading places for guest:', error);
            UI.showError('Failed to load places. Please try again.');
        }
    },

    /**
     * Setup price filter functionality
     */
    setupPriceFilter: function() {
        const priceFilter = document.getElementById('price-filter');
        if (priceFilter) {
            priceFilter.addEventListener('change', function(event) {
                const selectedPrice = event.target.value;
                Places.filterPlacesByPrice(selectedPrice);
            });
        }
    }
};

// Initialize application when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on the index page
    if (document.getElementById('places-list')) {
        // Initialize authentication and places loading for index page
        AuthUI.checkAuthentication();
    } else if (document.getElementById('place-details')) {
        // Initialize place details page
        PlaceDetails.initializePlaceDetails();
        // Also update general auth UI for header
        UI.updateAuthUI();
    } else if (document.getElementById('review-form-container')) {
        // Initialize add review page
        AddReview.initializeAddReviewPage();
        // Also update general auth UI for header
        UI.updateAuthUI();
    } else {
        // For other pages, just update the general auth UI
        UI.updateAuthUI();
    }

    // Handle login form submission
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async function(event) {
            event.preventDefault();
            
            // Get form data
            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value;
            
            // Basic validation
            if (!email || !password) {
                UI.showError('Please fill in all fields');
                return;
            }
            
            if (!isValidEmail(email)) {
                UI.showError('Please enter a valid email address');
                return;
            }
            
            // Show loading state
            const submitButton = loginForm.querySelector('button[type="submit"]');
            const originalText = submitButton.textContent;
            submitButton.disabled = true;
            submitButton.textContent = 'Logging in...';
            
            try {
                // Attempt login
                const result = await Auth.loginUser(email, password);
                
                if (result.success) {
                    UI.showSuccess('Login successful! Redirecting...');
                    
                    // Redirect after short delay
                    setTimeout(() => {
                        window.location.href = 'index.html';
                    }, 1000);
                } else {
                    UI.showError(result.message);
                }
            } catch (error) {
                UI.showError('An unexpected error occurred. Please try again.');
                console.error('Login error:', error);
            } finally {
                // Reset button state
                submitButton.disabled = false;
                submitButton.textContent = originalText;
            }
        });
    }

    // Handle review form submission (if on place details page)
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', async function(event) {
            event.preventDefault();
            
            if (!Auth.isAuthenticated()) {
                UI.showError('Please login to submit a review');
                return;
            }
            
            const rating = document.getElementById('rating').value;
            const comment = document.getElementById('comment').value.trim();
            
            if (!rating || !comment) {
                UI.showError('Please fill in all fields');
                return;
            }
            
            if (comment.length < 10) {
                UI.showError('Review must be at least 10 characters long');
                return;
            }
            
            // Here you would make an API call to submit the review
            // For now, we'll just show success and add to DOM
            UI.showSuccess('Review submitted successfully!');
            
            // Add review to page (mock implementation)
            const reviewsContainer = document.getElementById('reviews-container');
            if (reviewsContainer) {
                const reviewCard = document.createElement('div');
                reviewCard.className = 'review-card';
                reviewCard.innerHTML = `
                    <div class="review-header">
                        <span class="review-user">${Auth.getUserEmail()}</span>
                        <span class="review-rating">${'★'.repeat(rating)}${'☆'.repeat(5-rating)}</span>
                    </div>
                    <p class="review-comment">${comment}</p>
                `;
                reviewsContainer.appendChild(reviewCard);
            }
            
            // Reset form
            reviewForm.reset();
        });
    }
});

// Place Details Management
const PlaceDetails = {
    /**
     * Get place ID from URL parameters
     */
    getPlaceIdFromURL: function() {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get('id');
    },

    /**
     * Fetch place details from API
     */
    fetchPlaceDetails: async function(token, placeId) {
        try {
            const headers = {
                'Content-Type': 'application/json'
            };

            // Include token if provided
            if (token) {
                headers['Authorization'] = `Bearer ${token}`;
            }

            const response = await fetch(`${API_BASE_URL}/places/${placeId}`, {
                method: 'GET',
                headers: headers
            });

            if (response.ok) {
                const place = await response.json();
                return { success: true, data: place };
            } else {
                console.log('API request failed, using mock data');
                // Fallback to mock data if API fails
                const mockPlace = this.getMockPlaceDetails(placeId);
                return { success: true, data: mockPlace };
            }
        } catch (error) {
            console.error('Error fetching place details:', error);
            console.log('Using mock data due to error');
            // Fallback to mock data
            const mockPlace = this.getMockPlaceDetails(placeId);
            return { success: true, data: mockPlace };
        }
    },

    /**
     * Get mock place details for development/testing
     */
    getMockPlaceDetails: function(placeId) {
        const mockPlaces = {
            '1': {
                id: '1',
                title: 'Cozy Downtown Apartment',
                description: 'A beautiful and cozy apartment located in the heart of downtown. Perfect for business travelers and tourists alike. Walking distance to restaurants, shopping, and major attractions. The space features modern amenities and comfortable furnishings.',
                price_per_night: 120,
                city: 'New York',
                country: 'USA',
                owner: { first_name: 'John', last_name: 'Doe' },
                amenities: [
                    { name: 'Wi-Fi', icon: 'images/icon_wifi.png' },
                    { name: '2 Bedrooms', icon: 'images/icon_bed.png' },
                    { name: '2 Bathrooms', icon: 'images/icon_bath.png' },
                    { name: 'Kitchen', icon: null },
                    { name: 'Parking', icon: null }
                ],
                reviews: [
                    {
                        id: '1',
                        user: { first_name: 'Alice', last_name: 'Johnson' },
                        rating: 5,
                        comment: 'Absolutely loved staying here! The location is perfect and the apartment is exactly as described. John was a wonderful host.'
                    },
                    {
                        id: '2',
                        user: { first_name: 'Bob', last_name: 'Smith' },
                        rating: 4,
                        comment: 'Great place overall. Very clean and comfortable. Only minor issue was the wifi could be faster, but everything else was perfect.'
                    },
                    {
                        id: '3',
                        user: { first_name: 'Carol', last_name: 'Williams' },
                        rating: 5,
                        comment: 'Fantastic apartment in a prime location. Would definitely stay here again. The amenities were great and check-in was smooth.'
                    }
                ]
            },
            '2': {
                id: '2',
                title: 'Mountain View Cabin',
                description: 'Escape to this peaceful mountain cabin with stunning views and fresh air. Perfect for nature lovers and those seeking a quiet retreat. Features include a fireplace, full kitchen, and hiking trails nearby.',
                price_per_night: 85,
                city: 'Aspen',
                country: 'USA',
                owner: { first_name: 'Jane', last_name: 'Smith' },
                amenities: [
                    { name: 'Wi-Fi', icon: 'images/icon_wifi.png' },
                    { name: '3 Bedrooms', icon: 'images/icon_bed.png' },
                    { name: '2 Bathrooms', icon: 'images/icon_bath.png' },
                    { name: 'Fireplace', icon: null },
                    { name: 'Mountain View', icon: null }
                ],
                reviews: [
                    {
                        id: '4',
                        user: { first_name: 'David', last_name: 'Brown' },
                        rating: 5,
                        comment: 'Amazing mountain views and such a peaceful location. Perfect for a weekend getaway!'
                    }
                ]
            },
            '3': {
                id: '3',
                title: 'Beachfront Villa',
                description: 'Luxurious beachfront villa with direct beach access. Wake up to ocean views and fall asleep to the sound of waves. Perfect for families and groups looking for a premium beach vacation.',
                price_per_night: 200,
                city: 'Miami',
                country: 'USA',
                owner: { first_name: 'Mike', last_name: 'Johnson' },
                amenities: [
                    { name: 'Wi-Fi', icon: 'images/icon_wifi.png' },
                    { name: '4 Bedrooms', icon: 'images/icon_bed.png' },
                    { name: '3 Bathrooms', icon: 'images/icon_bath.png' },
                    { name: 'Beach Access', icon: null },
                    { name: 'Pool', icon: null }
                ],
                reviews: [
                    {
                        id: '5',
                        user: { first_name: 'Emma', last_name: 'Davis' },
                        rating: 5,
                        comment: 'Absolutely stunning beachfront location! The villa exceeded all expectations. Perfect for our family vacation.'
                    }
                ]
            }
        };

        return mockPlaces[placeId] || mockPlaces['1'];
    },

    /**
     * Display place details in the DOM
     */
    displayPlaceDetails: function(place) {
        // Hide loading message
        const loadingMessage = document.getElementById('loading-place');
        if (loadingMessage) {
            loadingMessage.style.display = 'none';
        }

        // Show place details container
        const placeDetailsContainer = document.getElementById('place-details');
        if (placeDetailsContainer) {
            placeDetailsContainer.style.display = 'block';
        }

        // Populate place information
        const titleElement = document.getElementById('place-title');
        if (titleElement) titleElement.textContent = place.title;

        const hostElement = document.getElementById('host-name');
        if (hostElement) {
            hostElement.textContent = `${place.owner.first_name} ${place.owner.last_name}`;
        }

        const locationElement = document.getElementById('place-location');
        if (locationElement) {
            locationElement.textContent = `${place.city}, ${place.country}`;
        }

        const priceElement = document.getElementById('place-price');
        if (priceElement) {
            priceElement.textContent = `$${place.price_per_night} per night`;
        }

        const descriptionElement = document.getElementById('place-description');
        if (descriptionElement) {
            descriptionElement.textContent = place.description;
        }

        // Display amenities
        this.displayAmenities(place.amenities || []);

        // Display reviews
        this.displayReviews(place.reviews || []);

        // Setup add review link
        this.setupAddReviewLink(place.id);
    },

    /**
     * Display amenities
     */
    displayAmenities: function(amenities) {
        const amenitiesList = document.getElementById('amenities-list');
        if (!amenitiesList) return;

        amenitiesList.innerHTML = '';

        amenities.forEach(amenity => {
            const span = document.createElement('span');
            span.className = 'amenity-tag';

            if (amenity.icon) {
                const img = document.createElement('img');
                img.src = amenity.icon;
                img.alt = amenity.name;
                img.className = 'amenity-icon';
                span.appendChild(img);
            }

            span.appendChild(document.createTextNode(amenity.name));
            amenitiesList.appendChild(span);
        });
    },

    /**
     * Display reviews
     */
    displayReviews: function(reviews) {
        const reviewsContainer = document.getElementById('reviews-container');
        const reviewsSection = document.getElementById('reviews-section');

        if (!reviewsContainer || !reviewsSection) return;

        // Show reviews section
        reviewsSection.style.display = 'block';

        reviewsContainer.innerHTML = '';

        if (reviews.length === 0) {
            reviewsContainer.innerHTML = '<p class="no-reviews">No reviews yet. Be the first to review this place!</p>';
            return;
        }

        reviews.forEach(review => {
            const reviewCard = document.createElement('div');
            reviewCard.className = 'review-card';

            const stars = '★'.repeat(review.rating) + '☆'.repeat(5 - review.rating);

            reviewCard.innerHTML = `
                <div class="review-header">
                    <span class="review-user">${review.user.first_name} ${review.user.last_name}</span>
                    <span class="review-rating">${stars}</span>
                </div>
                <p class="review-comment">${review.comment}</p>
            `;

            reviewsContainer.appendChild(reviewCard);
        });
    },

    /**
     * Check authentication and show/hide add review form
     */
    checkAuthenticationForPlace: function() {
        const token = CookieManager.getCookie('token');
        const addReviewSection = document.getElementById('add-review');

        if (!token) {
            // User not authenticated - hide add review form
            if (addReviewSection) {
                addReviewSection.style.display = 'none';
            }
            return null;
        } else {
            // User authenticated - show add review form
            if (addReviewSection) {
                addReviewSection.style.display = 'block';
            }
            return token;
        }
    },

    /**
     * Setup add review link with correct place ID
     */
    setupAddReviewLink: function(placeId) {
        const addReviewLink = document.getElementById('add-review-link');
        if (addReviewLink) {
            addReviewLink.href = `add_review.html?place_id=${placeId}`;
        }
    },

    /**
     * Initialize place details page
     */
    initializePlaceDetails: async function() {
        // Get place ID from URL
        const placeId = this.getPlaceIdFromURL();
        
        if (!placeId) {
            UI.showError('Place ID not found in URL');
            return;
        }

        // Check authentication
        const token = this.checkAuthenticationForPlace();

        try {
            // Fetch place details
            const result = await this.fetchPlaceDetails(token, placeId);
            
            if (result.success) {
                this.displayPlaceDetails(result.data);
            } else {
                UI.showError('Failed to load place details');
            }
        } catch (error) {
            console.error('Error initializing place details:', error);
            UI.showError('An error occurred while loading place details');
        }
    }
};

// Add Review Management
const AddReview = {
    /**
     * Check authentication and redirect if not authenticated
     */
    checkAuthenticationForAddReview: function() {
        const token = CookieManager.getCookie('token');
        
        if (!token) {
            // User not authenticated - redirect to index page
            UI.showError('You must be logged in to add a review. Redirecting...');
            setTimeout(() => {
                window.location.href = 'index.html';
            }, 2000);
            return null;
        }
        
        return token;
    },

    /**
     * Get place ID from URL parameters (supports both 'id' and 'place_id')
     */
    getPlaceIdFromURL: function() {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get('place_id') || urlParams.get('id');
    },

    /**
     * Load place information for review form
     */
    loadPlaceInfoForReview: async function(token, placeId) {
        try {
            // Try to fetch from API first
            const result = await PlaceDetails.fetchPlaceDetails(token, placeId);
            
            if (result.success) {
                const place = result.data;
                
                // Update place info display
                const titleElement = document.getElementById('place-title');
                if (titleElement) titleElement.textContent = place.title;

                const hostElement = document.getElementById('host-name');
                if (hostElement) {
                    hostElement.textContent = `${place.owner.first_name} ${place.owner.last_name}`;
                }

                return place;
            } else {
                throw new Error('Failed to load place information');
            }
        } catch (error) {
            console.error('Error loading place info:', error);
            UI.showError('Failed to load place information');
            return null;
        }
    },

    /**
     * Submit review to API
     */
    submitReview: async function(token, placeId, reviewData) {
        try {
            const response = await fetch(`${API_BASE_URL}/places/${placeId}/reviews`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(reviewData)
            });

            const data = await response.json();

            if (response.ok) {
                return { success: true, data: data };
            } else {
                return { 
                    success: false, 
                    message: data.message || 'Failed to submit review' 
                };
            }
        } catch (error) {
            console.error('Error submitting review:', error);
            return { 
                success: false, 
                message: 'Network error. Please check your connection and try again.' 
            };
        }
    },

    /**
     * Handle review form submission
     */
    handleReviewFormSubmission: async function(event) {
        event.preventDefault();
        
        // Double-check authentication
        const token = this.checkAuthenticationForAddReview();
        if (!token) return;

        // Get place ID
        const placeId = this.getPlaceIdFromURL();
        if (!placeId) {
            UI.showError('Place ID not found in URL');
            return;
        }

        // Get form data
        const rating = document.getElementById('rating').value;
        const comment = document.getElementById('comment').value.trim();
        const recommend = document.getElementById('recommend')?.value;

        // Validation
        if (!rating || !comment) {
            UI.showError('Please fill in all required fields');
            return;
        }

        if (comment.length < 10) {
            UI.showError('Review must be at least 10 characters long');
            return;
        }

        if (rating < 1 || rating > 5) {
            UI.showError('Please select a valid rating');
            return;
        }

        // Show loading state
        const submitButton = event.target.querySelector('button[type="submit"]');
        const originalText = submitButton.textContent;
        submitButton.disabled = true;
        submitButton.textContent = 'Submitting...';

        try {
            // Prepare review data
            const reviewData = {
                rating: parseInt(rating),
                comment: comment
            };

            // Include recommend field if present
            if (recommend) {
                reviewData.recommend = recommend === 'yes';
            }

            // Submit review
            const result = await this.submitReview(token, placeId, reviewData);

            if (result.success) {
                UI.showSuccess('Review submitted successfully! Redirecting...');
                
                // Clear form
                document.getElementById('review-form').reset();
                
                // Redirect back to place details after delay
                setTimeout(() => {
                    window.location.href = `place.html?id=${placeId}`;
                }, 2000);
            } else {
                UI.showError(result.message);
            }
        } catch (error) {
            UI.showError('An unexpected error occurred. Please try again.');
            console.error('Review submission error:', error);
        } finally {
            // Reset button state
            submitButton.disabled = false;
            submitButton.textContent = originalText;
        }
    },

    /**
     * Initialize add review page
     */
    initializeAddReviewPage: async function() {
        // Check authentication first
        const token = this.checkAuthenticationForAddReview();
        if (!token) return;

        // Get place ID
        const placeId = this.getPlaceIdFromURL();
        if (!placeId) {
            UI.showError('Place ID not found in URL. Redirecting to home...');
            setTimeout(() => {
                window.location.href = 'index.html';
            }, 3000);
            return;
        }

        try {
            // Load place information
            const place = await this.loadPlaceInfoForReview(token, placeId);
            
            if (place) {
                // Hide loading message and show form
                const loadingMessage = document.getElementById('loading-review-page');
                const formContainer = document.getElementById('review-form-container');
                
                if (loadingMessage) loadingMessage.style.display = 'none';
                if (formContainer) formContainer.style.display = 'block';

                // Setup form submission handler
                const reviewForm = document.getElementById('review-form');
                if (reviewForm) {
                    reviewForm.addEventListener('submit', (event) => {
                        this.handleReviewFormSubmission(event);
                    });
                }
            } else {
                UI.showError('Failed to load place information. Redirecting to home...');
                setTimeout(() => {
                    window.location.href = 'index.html';
                }, 3000);
            }
        } catch (error) {
            console.error('Error initializing add review page:', error);
            UI.showError('An error occurred while loading the page. Redirecting to home...');
            setTimeout(() => {
                window.location.href = 'index.html';
            }, 3000);
        }
    }
};

// Utility functions
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Export for use in other scripts if needed
window.HBnB = {
    Auth,
    CookieManager,
    UI,
    Places,
    PlaceDetails,
    AddReview,
    AuthUI,
    API_BASE_URL
};