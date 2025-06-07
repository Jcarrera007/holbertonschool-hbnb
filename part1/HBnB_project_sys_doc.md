# 🏨 HBnB Project – System Documentation

## 📌 Overview

HBnB is a simplified version of the Airbnb platform. This documentation provides a complete overview of the system architecture using both a **UML Sequence Diagram** and **UML Class Diagram**, detailing how components interact and the structure of the backend models.

---

## 1. System Sequence Diagram: Booking Process

### 🧱 Actors

- **User**: A person who uses the platform to search and book listings.
- **Website**: The front-end interface that communicates with the backend and other services.
- **Host**: The owner of the listing who approves or declines booking requests.
- **PaymentGateway**: Third-party service that processes transactions.
- **HBnB**: The backend system managing booking logic, support tickets, and data storage.

### 🔁 Sequence Flow

#### 1. **Search and Browse**
- `User → Website`: Search for listings
- `Website → User`: Display available properties
- `User → Website`: Select a property
- `Website → User`: Show property details

#### 2. **Booking Request**
- `User → Website`: Request booking
- `Website → Host`: Notify about booking request
- `Host → Website`: Accept/Decline booking
- `Website → User`: Notify booking status

#### 3. **If Booking Accepted**
- `User → Website`: Provide payment info
- `Website → PaymentGateway`: Process payment
- `PaymentGateway → Website`: Confirm payment
- `Website → User`: Confirm booking details
- `Website → HBnB`: Record booking

#### 4. **If Booking Declined**
- `Website → User`: Notify booking declined

#### 5. **Support Flow**
- `User → Website`: Ask for support
- `Website → User`: Provide help options
- `User → Website`: Raise a ticket
- `Website → HBnB`: Send support request
- `HBnB → Website`: Resolve issue
- `Website → User`: Update on ticket status

---

## 🧬 2. Class Diagram: Data Model Structure

All model classes inherit from a base class for consistency and tracking.

### 🧩 Base Class: `Model_1.0_HBnB`
Provides shared attributes and methods.

#### Attributes
- `id: str`
- `created_at: datetime`
- `updated_at: datetime`

#### Methods
- `save()`
- `to_dict()`

---

### 👤 `User`
Represents a system user.

#### Attributes
- `email: str`
- `password: str`
- `first_name: str`
- `last_name: str`

#### Relationships
- One user can:
  - Own many `Place`s
  - Write many `Review`s

---

### 🏠 `Place`
Represents a property listing.

#### Attributes
- `name: str`
- `description: str`
- `rooms: int`
- `price_by_night: float`
- `city_id: str`
- `user_id: str`

#### Relationships
- Belongs to a `City` and a `User`
- Has many `Review`s

---

### 🗣️ `Review`
Represents a user review of a property.

#### Attributes
- `text: str`
- `place_id: str`
- `user_id: str`

#### Relationships
- Belongs to a `Place` and a `User`

---

### 🏙️ `City`
Represents a city.

#### Attributes
- `name: str`
- `state_id: str`

#### Relationships
- Belongs to one `State`
- Has many `Place`s

---

### 🌍 `State`
Represents a region or state.

#### Attributes
- `name: str`

#### Relationships
- Has many `City` objects

---

## 📊 Summary of Relationships

- All classes inherit from `Model_1.0_HBnB`.
- **User ↔ Place**: One-to-many
- **User ↔ Review**: One-to-many
- **Place ↔ Review**: One-to-many
- **Place ↔ City**: Many-to-one
- **City ↔ State**: Many-to-one

---

## 📁 Project Purpose

This documentation supports the development of HBnB by providing a clear understanding of:

- The data flow during the booking lifecycle
- The structure and responsibilities of each data model
- The interactions between users, hosts, and the system

---

> 📌 *Generated as part of the HBnB architecture overview. Designed to support backend development, debugging, and onboarding.*

