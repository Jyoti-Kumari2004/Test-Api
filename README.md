# Event Management API

A modern, scalable REST API for managing events and participants built with **FastAPI**, **MySQL**, and clean architecture principles.

## ✨ Features

✅ **Event Management**

- Create, read, update, and delete events
- Event validation (future dates, date range validation)
- Comprehensive event details (venue, description, dates)

✅ **Participant Management**

- Register and manage participants
- Email validation
- Contact information tracking

✅ **Event Participation**

- Link participants to events
- Track event registrations
- Manage participation records

✅ **API Documentation**

- Interactive Swagger UI at `/docs`
- ReDoc documentation at `/redoc`
- Auto-generated OpenAPI schema

✅ **Production-Ready**

- Clean 3-tier architecture
- Input validation with Pydantic
- Error handling with meaningful responses
- SQLAlchemy ORM abstraction
- Async-ready with FastAPI

---

## 🏗 Architecture

This project follows a **3-Tier Layered Architecture**:

```
┌─────────────────────────────────────────┐
│       Routes Layer (API Endpoints)      │
│   • eventRoutes.py                      │
│   • participantRoutes.py                │
│   • eventParticipationRoutes.py         │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│      Services Layer (Business Logic)    │
│   • eventService.py                     │
│   • userService.py                      │
│   • eventParticipationService.py        │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│   Repository Layer (Data Access)        │
│   • baseRepo.py                         │
│   • eventRepo.py                        │
│   • participantRepo.py                  │
│   • eventParticipationRepo.py           │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│        MySQL Database (ContactDB)       │
└─────────────────────────────────────────┘
```

**Benefits:**

- **Separation of Concerns**: Each layer has a single responsibility
- **Testability**: Layers can be unit tested independently
- **Maintainability**: Changes in one layer don't affect others
- **Scalability**: Easy to extend with new features

For detailed system design explanation, see [SYSTEM_DESIGN.md](SYSTEM_DESIGN.md)

---

## 📦 Prerequisites

- **Python**: 3.9 or higher
- **MySQL**: 8.0 or higher
- **pip**: Package manager for Python
- **Virtual Environment**: venv or virtualenv

---

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/pranshukumar777/Test-Api.git
cd Test-Api
```

### 2. Create Virtual Environment

```bash
# On Windows
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# On macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Key Dependencies:**

- `fastapi` - Modern web framework
- `uvicorn` - ASGI server
- `sqlalchemy` - ORM
- `pymysql` - MySQL connector
- `pydantic` - Data validation
- `cryptography` - Secure authentication

### 4. Set Up Database

Create database and tables:

```sql
-- Create database
CREATE DATABASE IF NOT EXISTS ContactDB;
USE ContactDB;

-- Create tables
CREATE TABLE event (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(15) NOT NULL,
    venue VARCHAR(255) NOT NULL,
    startDate DATE NOT NULL,
    endDate DATE NOT NULL,
    description VARCHAR(255) NOT NULL
);

CREATE TABLE participant (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(15) NOT NULL,
    contact VARCHAR(20) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE event_participation (
    eventId INT NOT NULL,
    participantId INT NOT NULL,
    PRIMARY KEY (eventId, participantId),
    FOREIGN KEY (eventId) REFERENCES event(id),
    FOREIGN KEY (participantId) REFERENCES participant(id)
);
```

### 5. Configure Database Connection

Update `app/repos/baseRepo.py`:

```python
class BaseRepo:
    engine: object

    def __init__(self):
        self.engine = create_engine(
            "mysql+pymysql://root:your_password@localhost/ContactDB"
        )
```

**Connection String Format:**

```
mysql+pymysql://username:password@host:port/database_name
```

---

## ▶️ Running the Application

### Start the Server

```bash
# Navigate to project root
cd Test-api

# Run with auto-reload (development)
uvicorn app.main:app --reload

# Run without auto-reload (production)
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Access the API

- **Base URL**: http://127.0.0.1:8000
- **Swagger UI**: http://127.0.0.1:8000/docs
---

## 📡 API Endpoints

### Event Endpoints

| Method | Endpoint      | Description      |
| ------ | ------------- | ---------------- |
| GET    | `/event/{id}` | Get event by ID  |
| POST   | `/event`      | Create new event |
| PUT    | `/event/{id}` | Update event     |
| DELETE | `/event/{id}` | Delete event     |

#### Create Event

```bash
curl -X POST "http://127.0.0.1:8000/event" \
  -H "Content-Type: application/json" \
  -d '{
    "id": 1,
    "name": "Tech Summit",
    "venue": "Convention Center",
    "startDate": "2026-05-15",
    "endDate": "2026-05-16",
    "description": "Annual technology conference with industry experts"
  }'
```

#### Get Event

```bash
curl -X GET "http://127.0.0.1:8000/event/1"
```

### Participant Endpoints

| Method | Endpoint            | Description           |
| ------ | ------------------- | --------------------- |
| GET    | `/home/{id}`        | Get participant by ID |
| POST   | `/participant`      | Register participant  |
| PUT    | `/participant/{id}` | Update participant    |
| DELETE | `/participant/{id}` | Delete participant    |

#### Register Participant

```bash
curl -X POST "http://127.0.0.1:8000/participant" \
  -H "Content-Type: application/json" \
  -d '{
    "id": 1,
    "name": "John Doe",
    "contact": "+1234567890",
    "email": "john@example.com"
  }'
```

### Event Participation Endpoints

| Method | Endpoint                                       | Description                    |
| ------ | ---------------------------------------------- | ------------------------------ |
| POST   | `/event/{eventId}/participant/{participantId}` | Register participant for event |

#### Register for Event

```bash
curl -X POST "http://127.0.0.1:8000/event/1/participant/1"
```

### Layer Responsibilities

**Models** (`models/`)

- Define data structures with Pydantic
- Implement validation rules
- Type safety and documentation

**Routes** (`routes/`)

- Define API endpoints
- Handle HTTP requests
- Delegate to services

**Services** (`services/`)

- Implement business logic
- Orchestrate repository calls
- Handle data transformations

**Repositories** (`repos/`)

- Abstract database operations
- Execute SQL queries
- Transform database rows to models

---

## 💾 Database Schema

### Event Table

```sql
CREATE TABLE event (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(15) NOT NULL,           -- Event name (max 15 chars)
    venue VARCHAR(255) NOT NULL,         -- Event location
    startDate DATE NOT NULL,             -- Event start date
    endDate DATE NOT NULL,               -- Event end date
    description VARCHAR(255) NOT NULL   -- Event description (min 10 chars)
);
```

### Participant Table

```sql
CREATE TABLE participant (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(15) NOT NULL,           -- Participant name (max 15 chars)
    contact VARCHAR(20) NOT NULL,        -- Phone number
    email VARCHAR(255) NOT NULL UNIQUE   -- Email address (validated)
);
```

### Validation Rules

**Event Validation:**

- `startDate` must be today or in the future
- `endDate` must be after `startDate`
- `name` max length: 15 characters
- `description` min length: 10 characters

**Participant Validation:**

- `email` must be valid email format
- `name` max length: 15 characters
- `email` must be unique

---

## 📚 Data Models

### Event Model

```python
from pydantic import BaseModel, Field

class Event(BaseModel):
    id: int = Field(gt=0)                                    # Must be positive
    name: str = Field(max_length=15)                         # Max 15 characters
    venue: str                                               # Location string
    startDate: date                                          # Future date required
    endDate: date                                            # Must be after startDate
    description: str = Field(min_length=10)                  # Min 10 characters
```

### Participant Model

```python
from pydantic import BaseModel, Field, EmailStr

class Participant(BaseModel):
    id: int = Field(gt=0)                                    # Must be positive
    name: str = Field(max_length=15)                         # Max 15 characters
    contact: str                                             # Phone number
    email: EmailStr                                          # Valid email format
```

---

## 🧪 Testing Endpoints with Swagger UI

#### Step 1: Start Server

```bash
uvicorn app.main:app --reload
```

#### Step 2: Open Swagger UI

Navigate to: http://127.0.0.1:8000/docs

#### Step 3: Test Endpoints

- Click on an endpoint to expand it
- Click "Try it out" button
- Fill in parameters and request body
- Click "Execute" to send request
- View response

---

## Swagger API Interface

<img width="1756" height="858" alt="Screenshot 2026-04-20 115748" src="https://github.com/user-attachments/assets/7819cc5f-119d-4ec7-820d-1c98b4ac7a7f" />
_Swagger UI showing Event management endpoints_

<img width="1500" height="929" alt="Screenshot 2026-04-20 120625" src="https://github.com/user-attachments/assets/9241215d-ce07-4fcc-bd01-6fb6ddadc0fb" />
_Example response from Event GET endpoint_

---


## 🔗 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [MySQL Documentation](https://dev.mysql.com/doc/)

---
