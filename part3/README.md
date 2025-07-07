# 🏠 HBnB Part 3: Authenticated User Access 🔐

<div align="center">

![Python](https://img.shields.io/badge/python-v3.11+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-v3.1.1-green.svg)
![JWT](https://img.shields.io/badge/JWT-Authentication-orange.svg)
![Tests](https://img.shields.io/badge/Tests-16%2F16%20Passing-brightgreen.svg)
![Status](https://img.shields.io/badge/Status-Complete-success.svg)

**🚀 Secure API endpoints with JWT authentication and comprehensive business logic validation**

[Features](#-features) • [Quick Start](#-quick-start) • [API Documentation](#-api-documentation) • [Testing](#-testing) • [Security](#-security)

</div>

---

## 🎯 **Project Overview**

This is **Part 3** of the HBnB (Holberton School AirBnB) project, implementing **authenticated user access** for a Flask-based API. The system provides secure endpoints for managing users, places, and reviews with JWT-based authentication and comprehensive business logic validation.

### 🌟 **What Makes This Special**

- **🔐 JWT Authentication** - Secure token-based user authentication
- **👥 User Management** - Protected user profile updates with ownership validation
- **🏡 Place Management** - Secure place creation, updates, and deletion
- **⭐ Review System** - Protected reviews with business logic enforcement
- **🌐 Public Access** - Read-only endpoints remain public for browsing
- **🧪 Comprehensive Testing** - 16 automated tests covering all security scenarios

---

## ✨ **Features**

### 🔒 **Authentication & Authorization**
- **JWT Token Authentication** with 24-hour expiration
- **User Login System** with secure password validation
- **Ownership-based Access Control** - users can only modify their own data

### 👤 **User Management**
- ✅ **Protected Profile Updates** - users can only update their own profiles
- ❌ **Email/Password Protection** - critical fields cannot be modified via API
- 🚫 **Cross-user Access Prevention** - unauthorized access blocked

### 🏠 **Place Management**
- ✅ **Authenticated Place Creation** - only logged-in users can create places
- 🔐 **Owner-only Updates/Deletion** - only place owners can modify their places
- 🌍 **Public Browsing** - anyone can view places and details

### 📝 **Review System**
- ✅ **Authenticated Review Creation** with business rules:
  - 🚫 **No Self-Reviews** - users cannot review their own places
  - 🚫 **No Duplicate Reviews** - users cannot review the same place twice
- 🔐 **Author-only Updates/Deletion** - only review authors can modify reviews
- 👀 **Public Review Access** - anyone can read reviews

---

## 🚀 **Quick Start**

### Prerequisites
- Python 3.11+
- Flask 3.1.1+
- Flask-RESTx
- Flask-JWT-Extended

### 📦 **Installation**

```bash
# Clone the repository
git clone <repository-url>
cd holbertonschool-hbnb/part3

# Install dependencies
pip install -r requirements.txt

# Start the server
python run.py
```

### 🌐 **Access Points**
- **API Server**: http://127.0.0.1:5000
- **Interactive Documentation**: http://127.0.0.1:5000/api/v1/
- **API Base URL**: http://127.0.0.1:5000

---

## 📚 **API Documentation**

### 🔓 **Public Endpoints**
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/users/` | List all users |
| `GET` | `/users/{id}` | Get user details |
| `GET` | `/places/` | List all places |
| `GET` | `/places/{id}` | Get place details |
| `GET` | `/reviews/` | List all reviews |
| `GET` | `/reviews/{id}` | Get review details |
| `GET` | `/reviews/places/{place_id}` | Get reviews for a place |

### 🔐 **Authentication**
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/auth/login` | User login (returns JWT token) |

### 🔒 **Protected Endpoints**
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `PUT` | `/users/{id}` | Update own profile | ✅ JWT + Ownership |
| `POST` | `/places/` | Create new place | ✅ JWT |
| `PUT` | `/places/{id}` | Update own place | ✅ JWT + Ownership |
| `DELETE` | `/places/{id}` | Delete own place | ✅ JWT + Ownership |
| `POST` | `/reviews/` | Create review | ✅ JWT + Business Rules |
| `PUT` | `/reviews/{id}` | Update own review | ✅ JWT + Ownership |
| `DELETE` | `/reviews/{id}` | Delete own review | ✅ JWT + Ownership |

---

## 🔐 **Security Features**

### 🛡️ **Authentication**
- **JWT Tokens** with secure secret key
- **24-hour token expiration** for security
- **Bearer token authorization** in headers

### 🚨 **Business Logic Validation**
- **Ownership Enforcement** - users can only modify their own resources
- **Self-Review Prevention** - users cannot review their own places
- **Duplicate Review Prevention** - one review per user per place
- **Critical Field Protection** - email/password cannot be modified via update API

### 🔒 **Access Control**
- **Resource-level Authorization** - fine-grained access control
- **Public Read Access** - browsing remains unrestricted
- **Private Write Access** - all modifications require authentication

---

## 🧪 **Testing**

### 🤖 **Automated Testing**
Run the comprehensive test suite:

```bash
python test_authenticated_endpoints.py
```

**Test Coverage: 16/16 Passing ✅**
- ✅ User authentication and authorization
- ✅ Protected user profile updates
- ✅ Unauthorized access prevention
- ✅ Place creation and ownership validation
- ✅ Review business logic enforcement
- ✅ Public endpoint accessibility

### 📋 **Manual Testing**
Use the manual testing guide:

```bash
python manual_test_guide.py
```

### 🎯 **Test Scenarios**
- **Authentication Flow** - Login and token validation
- **Ownership Validation** - Users can only modify their own data
- **Business Rules** - Self-review and duplicate prevention
- **Public Access** - Read endpoints work without authentication
- **Error Handling** - Proper status codes and error messages

---

## 📁 **Project Structure**

```
part3/
├── 📄 README.md                     # This file
├── 🚀 run.py                        # Application entry point
├── 📋 requirements.txt              # Python dependencies
├── 🧪 test_authenticated_endpoints.py # Comprehensive test suite
├── 📖 manual_test_guide.py          # Manual testing guide
├── 📊 TASK_COMPLETION_SUMMARY.md    # Implementation summary
├── 📝 AUTHENTICATED_ENDPOINTS_SUMMARY.md # Technical documentation
├── 
├── 📁 app/
│   ├── 🔧 __init__.py              # Flask app factory
│   └── 📁 models/                   # Data models
│       ├── 👤 user.py
│       ├── 🏠 place.py
│       ├── ⭐ review.py
│       └── 🏷️ amenity.py
│
└── 📁 api/
    └── 📁 v1/
        ├── 🔗 __init__.py          # API namespace registration
        ├── 🔐 auth.py              # Authentication endpoints
        ├── 👥 users.py             # User management endpoints
        ├── 🏡 places.py            # Place management endpoints
        ├── 📝 reviews.py           # Review management endpoints
        └── 🏷️ amenities.py         # Amenity endpoints
```

---

## 🛠️ **Technology Stack**

<div align="center">

| Technology | Purpose | Version |
|------------|---------|---------|
| ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) | Backend Language | 3.11+ |
| ![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white) | Web Framework | 3.1.1 |
| ![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=JSON%20web%20tokens&logoColor=white) | Authentication | Latest |
| ![Swagger](https://img.shields.io/badge/Swagger-85EA2D?style=for-the-badge&logo=swagger&logoColor=black) | API Documentation | via Flask-RESTx |

</div>

---

## 📈 **Usage Examples**

### 🔑 **Authentication Flow**

```bash
# 1. Create a user
curl -X POST http://127.0.0.1:5000/users/ \
  -H "Content-Type: application/json" \
  -d '{"first_name":"John","last_name":"Doe","email":"john@test.com","password":"secure123"}'

# 2. Login to get JWT token
curl -X POST http://127.0.0.1:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"john@test.com","password":"secure123"}'

# 3. Use token for protected operations
curl -X POST http://127.0.0.1:5000/places/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{"title":"My Place","price":100,"latitude":40.7128,"longitude":-74.0060}'
```

### 🏠 **Place Management**

```bash
# Create a place (requires authentication)
curl -X POST http://127.0.0.1:5000/places/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"title":"Beach House","description":"Beautiful oceanfront","price":200,"latitude":25.7617,"longitude":-80.1918}'

# Browse places (public access)
curl -X GET http://127.0.0.1:5000/places/
```

### ⭐ **Review System**

```bash
# Create a review (requires authentication + business rules)
curl -X POST http://127.0.0.1:5000/reviews/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"text":"Amazing place!","rating":5,"place_id":"PLACE_ID"}'

# Browse reviews (public access)
curl -X GET http://127.0.0.1:5000/reviews/places/PLACE_ID
```

---

## 🎉 **Success Metrics**

<div align="center">

### 📊 **Test Results**
![Tests](https://img.shields.io/badge/Total%20Tests-16-blue)
![Passing](https://img.shields.io/badge/Passing-16-brightgreen)
![Failing](https://img.shields.io/badge/Failing-0-red)
![Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen)

### 🔐 **Security Features**
![JWT Auth](https://img.shields.io/badge/JWT%20Auth-✅-brightgreen)
![Ownership](https://img.shields.io/badge/Ownership%20Validation-✅-brightgreen)
![Business Rules](https://img.shields.io/badge/Business%20Rules-✅-brightgreen)
![Public Access](https://img.shields.io/badge/Public%20Access-✅-brightgreen)

</div>

---

## 📄 **Documentation**

- 📊 **[Task Completion Summary](TASK_COMPLETION_SUMMARY.md)** - Detailed implementation overview
- 📝 **[Authenticated Endpoints Summary](AUTHENTICATED_ENDPOINTS_SUMMARY.md)** - Technical documentation
- 🧪 **[Testing Guide](manual_test_guide.py)** - Step-by-step manual testing
- 🔧 **[API Tests](test_authenticated_endpoints.py)** - Automated test suite

---

## 🤝 **Contributing**

This project is part of the Holberton School curriculum. For educational purposes, please follow the project guidelines and requirements.

---

## 📜 **License**

This project is part of the Holberton School curriculum. Educational use only.

---

<div align="center">

**🚀 Built with ❤️ for secure, scalable API development**

[![Python](https://img.shields.io/badge/Made%20with-Python-blue)](https://python.org)
[![Flask](https://img.shields.io/badge/Powered%20by-Flask-green)](https://flask.palletsprojects.com/)
[![JWT](https://img.shields.io/badge/Secured%20with-JWT-orange)](https://jwt.io/)

</div>
