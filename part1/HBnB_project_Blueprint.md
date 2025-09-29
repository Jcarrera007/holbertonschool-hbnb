# HBnB Project Technical Blueprint

## Introduction

The HBnB project is a simplified clone of the Airbnb platform, designed to allow users to search, view, and book properties online. This technical document compiles and explains the system's architectural design, including high-level package structure, business logic data models, and API interaction flows. It serves as a comprehensive blueprint that will guide implementation, testing, and future enhancements.

## 1. High-Level Architecture

### Overview

HBnB follows a **three-layered architecture**:

* **Presentation Layer**: Handles user interface and API endpoints.
* **Business Logic Layer**: Processes data and enforces application rules.
* **Persistence Layer**: Manages database storage and retrieval.

The **facade pattern** is used to encapsulate the interactions between layers, simplifying the interface and promoting separation of concerns.

### Diagram: High-Level Package Structure

(*Include the package diagram image here*)

### Explanatory Notes

* **Website (Presentation)**: Manages UI rendering and RESTful API endpoints.
* **Models (Business Logic)**: Encapsulate domain logic such as Place, User, City, etc.
* **Database Layer**: Manages data persistence.
* **HBnB Facade**: Central interface used by the Presentation Layer to access business logic operations.

---

## 2. Business Logic Layer

### Overview

The core of the HBnB system lies in its well-structured data models, which represent entities and their relationships. All models inherit from a base model class to ensure consistency.

### Diagram: Class Diagram

(*Include the class diagram image here*)

### Explanatory Notes

#### Base Class: `Model_1.0_HBnB`

* Provides shared attributes like `id`, `created_at`, and `updated_at`.
* Implements `save()` and `to_dict()` methods.

#### User

* Represents individuals using the platform.
* Can create Places and write Reviews.

#### Place

* Represents a property listing.
* Connected to a City and owned by a User.

#### Review

* Linked to both Place and User.
* Captures user feedback.

#### City and State

* Hierarchical geographic structure.
* Cities belong to States; Places belong to Cities.

---

## 3. API Interaction Flow

### Overview

This section describes how users interact with the platform from searching for properties to completing a booking, and optionally, requesting support.

### Diagram: Booking Process Sequence Diagram

(*Include the sequence diagram image here*)

### Explanatory Notes

#### Key Interactions

1. **Search Phase**: Users browse listings using filters and criteria.
2. **Booking Request**: Users send a request; hosts are notified to approve or decline.
3. **Payment Process**: Payments are processed only after approval.
4. **Support Flow**: Users can submit support tickets which are routed through HBnB's internal system.

#### Design Decisions

* Booking is conditional on host approval to avoid misuse.
* Asynchronous notification ensures flexibility in communication.
* Payment confirmation is required before recording the booking.

---

## Conclusion

This document provides a comprehensive, unified view of the HBnB application's architecture. It is intended to serve as a reference throughout the implementation and testing phases. All design choices promote scalability, maintainability, and clarity of system interactions.