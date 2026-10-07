# Signal Clone — Backend

A backend implementation of a Signal-inspired secure messaging platform built with **FastAPI, SQLAlchemy, SQLite, JWT authentication, and WebSockets**.

The backend follows a layered architecture with **Repository, Service, Strategy, Factory, Observer/Pub-Sub, and Dependency Injection patterns** to keep business logic modular and maintainable.

---

## 1. Tech Stack

- **Python**
- **FastAPI**
- **SQLAlchemy**
- **SQLite**
- **Pydantic**
- **JWT**
- **WebSockets**
- **Uvicorn**

---

## 2. Current Features

The following functionality has been implemented:

- User registration
- Mock OTP authentication
- JWT-based authentication
- Current-user authentication dependency
- Contact management
- Contact search
- Direct messaging
- Persistent message storage
- Message status management
- Real-time WebSocket messaging
- WebSocket authentication
- Multiple WebSocket connections per user
- Event-based message broadcasting

### Current message lifecycle

```text
SENT → DELIVERED → READ
```

The status API is currently available, while automatic delivery/read transitions are planned for the next phase.

---

## 3. Project Structure

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── constants.py
│   │   └── security.py
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── seed.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── contact.py
│   │   └── message.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── contact.py
│   │   └── message.py
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── user_repository.py
│   │   ├── contact_repository.py
│   │   └── message_repository.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── contact_service.py
│   │   └── message_service.py
│   │
│   ├── strategies/
│   │   ├── __init__.py
│   │   ├── message_strategy.py
│   │   ├── direct_message_strategy.py
│   │   └── message_strategy_factory.py
│   │
│   ├── events/
│   │   ├── __init__.py
│   │   ├── event.py
│   │   └── message_event.py
│   │
│   ├── websocket/
│   │   ├── __init__.py
│   │   ├── manager.py
│   │   └── handler.py
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── contacts.py
│   │   └── messages.py
│   │
│   └── dependencies.py
│
├── tests/
├── .env
├── requirements.txt
├── signal.db
└── README.md
```

---

# 4. Architecture

The backend follows a layered architecture:

```text
                    ┌──────────────────┐
                    │     Client       │
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │     Routers      │
                    │   HTTP / WS      │
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │    Services      │
                    │ Business Logic   │
                    └────────┬─────────┘
                             │
              ┌──────────────▼──────────────┐
              │       Strategy / Factory    │
              │     Message Processing      │
              └──────────────┬──────────────┘
                             │
                    ┌────────▼─────────┐
                    │   Repositories   │
                    │  Data Access     │
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │      SQLite      │
                    └──────────────────┘
```

For real-time communication:

```text
WebSocket
    │
    ▼
WebSocket Handler
    │
    ▼
Message Service
    │
    ▼
Repository
    │
    ▼
SQLite
    │
    ▼
Message Event
    │
    ▼
Event Publisher
    │
    ▼
WebSocket Manager
    │
    ├──────────► Sender
    │
    └──────────► Receiver
```

---

# 5. Design Principles

The implementation intentionally follows SOLID principles.

## Single Responsibility Principle

Each layer has a specific responsibility:

- **Router** → HTTP/WebSocket interface
- **Service** → business logic
- **Repository** → database operations
- **Strategy** → message-specific behavior
- **WebSocket Manager** → connection management
- **Event Publisher** → event distribution

---

## Open/Closed Principle

The messaging system uses strategies so additional message types can be introduced without significantly modifying existing messaging logic.

Current:

```text
MessageStrategy
      │
      └── DirectMessageStrategy
```

Future:

```text
MessageStrategy
      ├── DirectMessageStrategy
      └── GroupMessageStrategy
```

---

## Dependency Inversion

Business logic depends on abstractions where appropriate rather than coupling the entire application directly to HTTP or WebSocket implementations.

FastAPI dependency injection is used for database sessions and authenticated users.

---

# 6. Design Patterns

## Repository Pattern

Database operations are isolated inside repositories.

Example:

```python
user_repository.get_by_id(user_id)
```

The service layer does not need to know how SQLAlchemy queries are constructed.

---

## Service Layer Pattern

Services contain application/business logic.

Example:

```text
Contact Router
      ↓
Contact Service
      ↓
Contact Repository
```

This prevents routers from becoming large collections of business logic.

---

## Strategy Pattern

Messaging behavior is represented using strategies.

```text
MessageStrategy
       │
       └── DirectMessageStrategy
```

This allows group messaging and other message types to be added later.

---

## Factory Pattern

`MessageStrategyFactory` determines which messaging strategy should be used based on the request.

```text
Message Request
      │
      ▼
Strategy Factory
      │
      ├── Direct Message
      │
      └── Group Message (future)
```

---

## Observer / Pub-Sub Pattern

Message creation produces an event:

```text
MessageCreatedEvent
```

The event publisher notifies subscribed handlers.

This keeps message persistence separate from real-time WebSocket delivery.

---

## Dependency Injection

FastAPI's dependency injection system is used for:

- Database sessions
- Authentication
- Current user retrieval

Example:

```python
current_user: User = Depends(get_current_user)
```

---

# 7. Database Schema

The current database contains:

### Users

```text
users
├── user_id
├── phone_number
├── username
├── profile_picture
├── status
└── last_seen
```

### Contacts

```text
contacts
├── contact_id
├── user_id
├── contact_user_id
└── created_at
```

### Messages

```text
messages
├── message_id
├── sender_id
├── receiver_id
├── group_id
├── content
├── media_url
├── timestamp
└── status
```

Direct messages currently use:

```text
sender_id   → required
receiver_id → required
group_id    → NULL
```

Group messaging will be introduced in a later phase.

---

# 8. Authentication

Authentication uses:

```text
Phone Number
     ↓
Login Request
     ↓
Mock OTP
     ↓
OTP Verification
     ↓
JWT
```

For development, the fixed OTP is:

```text
123456
```

JWT tokens contain the authenticated user's ID.

Protected HTTP endpoints require:

```text
Authorization: Bearer <token>
```

---

# 9. Authentication Flow

### Registration

```http
POST /auth/register
```

Request:

```json
{
  "phone_number": "9876543210",
  "username": "alice"
}
```

---

### Request OTP

```http
POST /auth/login/request
```

Request:

```json
{
  "phone_number": "9876543210"
}
```

---

### Verify OTP

```http
POST /auth/login/verify
```

Request:

```json
{
  "phone_number": "9876543210",
  "otp": "123456"
}
```

Response:

```json
{
  "access_token": "<JWT>",
  "token_type": "bearer",
  "user_id": 1,
  "username": "alice"
}
```

---

# 10. Contact API

## Add Contact

```http
POST /contacts
```

```json
{
  "contact_user_id": 2
}
```

---

## List Contacts

```http
GET /contacts
```

Requires authentication.

---

## Search Contacts

```http
GET /contacts/search?q=alice
```

Searches usernames and phone numbers.

---

## Remove Contact

```http
DELETE /contacts/{contact_user_id}
```

---

# 11. Direct Messaging API

## Send Direct Message

```http
POST /messages/direct
```

```json
{
  "receiver_id": 2,
  "content": "Hello!",
  "media_url": null
}
```

---

## Get Conversation

```http
GET /messages/direct/{user_id}
```

Returns the conversation between the authenticated user and the specified user.

---

## Update Message Status

```http
PATCH /messages/{message_id}/status
```

```json
{
  "status": "READ"
}
```

Valid statuses:

```text
SENT
DELIVERED
READ
```

Statuses cannot move backwards.

---

# 12. WebSocket API

WebSocket endpoint:

```text
/ws?token=<JWT>
```

The JWT is validated before the connection is accepted.

---

## Connecting

```javascript
const ws = new WebSocket(
    "ws://localhost:8000/ws?token=<JWT>"
);
```

---

## Sending a Message

Client:

```json
{
  "type": "message.send",
  "receiver_id": 2,
  "content": "Hello!",
  "media_url": null
}
```

Server broadcasts:

```json
{
  "type": "message.new",
  "message": {
    "message_id": 1,
    "sender_id": 1,
    "receiver_id": 2,
    "group_id": null,
    "content": "Hello!",
    "media_url": null,
    "timestamp": "2026-10-07T10:30:00",
    "status": "SENT"
  }
}
```

---

# 13. Multiple Connections

The WebSocket manager maintains:

```python
dict[int, set[WebSocket]]
```

rather than a single connection per user.

Therefore one user can have multiple active sessions:

```text
User 1
 ├── Browser
 ├── Laptop
 └── Mobile
```

Messages can be delivered to all active connections.

---

# 14. Real-Time Event Architecture

When a message is sent:

```text
Client
  │
  │ message.send
  ▼
WebSocket Handler
  │
  ▼
Message Service
  │
  ▼
Message Strategy
  │
  ▼
Message Repository
  │
  ▼
SQLite
  │
  ▼
MessageCreatedEvent
  │
  ▼
EventPublisher
  │
  ▼
WebSocket Manager
  │
  ├──► Sender
  │
  └──► Receiver
```

This prevents the message service from becoming tightly coupled to WebSocket implementation details.

---

# 15. Environment Configuration

Create a `.env` file:

```env
APP_NAME=Signal Clone
DATABASE_URL=sqlite:///./signal.db
DEBUG=True

JWT_SECRET=change-this-secret-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

For production, `JWT_SECRET` must be replaced with a strong randomly generated secret.

---

# 16. Installation

Create and activate a virtual environment:

### Windows PowerShell

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

---

# 17. Running the Backend

From the `backend` directory:

```powershell
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

---

# 18. Database

SQLite is used as the database for the current implementation.

Database file:

```text
signal.db
```

Tables currently implemented:

```text
users
contacts
messages
```

SQLAlchemy automatically creates the tables when the application starts.

---

# 19. Testing

The project is structured to support unit and integration tests under:

```text
tests/
```

Planned test coverage includes:

```text
tests/
├── test_auth.py
├── test_messages.py
├── test_groups.py
└── test_contacts.py
```

Important scenarios include:

- Registration
- Duplicate users
- OTP verification
- Invalid JWT
- Contact creation/removal
- Direct messaging
- Invalid receivers
- Message status transitions
- WebSocket authentication
- Real-time message delivery

---

# 20. Development Roadmap

### Completed

- [x] Backend foundation
- [x] SQLite database
- [x] User model
- [x] Registration
- [x] Mock OTP authentication
- [x] JWT authentication
- [x] Current-user dependency
- [x] Contact management
- [x] Direct messaging
- [x] Message status management
- [x] WebSocket infrastructure
- [x] Real-time direct messaging
- [x] Event-based WebSocket notifications

### Upcoming

- [ ] Automatic delivery/read receipts
- [ ] Online/offline presence
- [ ] Typing indicators
- [ ] Group model
- [ ] Group members
- [ ] Group messaging
- [ ] Group admin operations
- [ ] Media handling
- [ ] Frontend integration
- [ ] Tests
- [ ] Production deployment
- [ ] Placeholder flows for calls, stories and linked devices

---

# 21. Security Notes

This project is a functional Signal-inspired clone and **does not currently implement Signal Protocol end-to-end encryption**.

The current implementation provides:

- JWT authentication
- Authenticated WebSocket connections
- Server-side authorization
- Persistent message storage
- Structured message status handling

Actual Signal-style end-to-end encryption would require a substantially more advanced cryptographic architecture involving identity keys, prekeys, session establishment, ratcheting, and encrypted message payloads.

For this assignment, those cryptographic workflows can be represented through appropriate placeholders.

---

# 22. API Documentation

Once the backend is running, FastAPI automatically provides interactive API documentation:

```text
http://localhost:8000/docs
```

Alternative ReDoc documentation:

```text
http://localhost:8000/redoc
```

---

# 23. Development Philosophy

The backend intentionally avoids unnecessary overengineering while maintaining clear separation of responsibilities.

The main goals are:

1. **Maintainability**
2. **Separation of concerns**
3. **Testability**
4. **Extensibility**
5. **Clear business logic**
6. **SOLID principles**
7. **Clean real-time communication**

The architecture is designed so that future features such as group messaging can be added without rewriting the existing direct messaging implementation.