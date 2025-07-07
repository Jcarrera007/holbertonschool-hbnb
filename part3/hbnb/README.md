# 🏨 HBnB – Modular Python Web Application

HBnB is a simplified clone of Airbnb, designed using a modular architecture in Python with Flask and Flask-RESTx. This project serves as a foundation for building scalable web applications using layered design patterns and clean code separation.

## 📦 Project Structure

```
hbnb/
├── app/
│   ├── api/                # RESTful API endpoints (v1/users, places, reviews, amenities)
│   ├── models/             # Business logic and core entities
│   ├── services/           # Facade for interacting with persistence and models
│   ├── persistence/        # In-memory data storage (replaced with SQLAlchemy in Part 3)
├── documentation/          # 📚 Complete project documentation
├── run.py                  # Application entry point
├── config.py               # App configuration
├── requirements.txt        # Project dependencies
├── README.md               # Project documentation
```

## 📚 Documentation

All detailed documentation has been organized in the [`documentation/`](./documentation/) folder:

- **[Documentation Index](./documentation/INDEX.md)** - Complete guide to all documentation
- **[Business Logic Summary](./documentation/BUSINESS_LOGIC_SUMMARY.md)** - Application architecture overview
- **[Password Implementation](./documentation/PASSWORD_IMPLEMENTATION_SUMMARY.md)** - Security features and password hashing
- **[API Testing Guide](./documentation/CURL_TESTING_GUIDE.md)** - Comprehensive cURL testing examples
- **[Quick Start Guide](./documentation/QUICK_START_CURL.md)** - Quick API reference
- **[Testing Reports](./documentation/TESTING_REPORTS.md)** - Test results and coverage
- **[WSL Testing Guide](./documentation/WSL_PASSWORD_TESTING.md)** - WSL-specific testing instructions

---

## 🧱 Architecture Overview

The application is divided into three primary layers:

- **Presentation Layer** (`api/`): Handles HTTP requests and responses using Flask-RESTx.
- **Business Logic Layer** (`models/`): Contains data models and validation rules.
- **Persistence Layer** (`persistence/`): Stores and retrieves objects (in-memory implementation provided).

A **Facade** class (`services/facade.py`) is used to coordinate interactions between these layers, providing a clean and unified API to the Presentation Layer.

---

## 🛠 Technologies Used

- **Python 3.9+**
- **Flask**
- **Flask-RESTx**
- **Modular Architecture**
- **Facade Design Pattern**

---

## 🧚‍♂️ Testing the Setup

To verify that the app is running:

- Visit `http://localhost:5000/api/v1/`
- You should see the interactive Swagger documentation interface (no routes implemented yet).

---

## 📚 Future Plans

- 🔄 Replace in-memory repositories with **SQLAlchemy** ORM.
- 🔡 Add input validation and error handling.
- 🔐 Implement authentication and authorization.
- 📊 Add unit tests and CI/CD integration.

---