# Signal Clone — Secure Messaging Platform

A full-stack, Signal-inspired secure messaging platform built as an SDE full-stack assignment.

The project aims to reproduce the core messaging experience of Signal, including user registration, contacts, one-to-one messaging, group conversations, real-time communication, message delivery/read states, and a privacy-focused interface.

> **Note:** This project is a functional Signal-inspired clone for educational/assignment purposes. It does not currently implement the Signal Protocol or production-grade end-to-end encryption.

---

## 1. Project Overview

The application provides a real-time messaging platform where users can:

- Register using a phone number and username
- Authenticate using a mock OTP
- Maintain contacts
- Search for users
- Send and receive direct messages
- View message timestamps
- Track message delivery/read status
- Communicate in real time using WebSockets
- Create and participate in group conversations
- Manage group members and administrators
- Use a Signal-inspired messaging interface

Additional Signal features such as calls, stories, linked devices, and advanced cryptography are represented as future/placeholder functionality where appropriate.

---

## 2. Tech Stack

### Frontend

- Next.js
- TypeScript
- React
- WebSocket client

### Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- WebSockets
- JWT

### Database

- SQLite

### Development

- Git
- GitHub
- Uvicorn

---

## 3. Repository Structure

```text
signal-clone/
│
├── backend/
│   ├── app/
│   ├── tests/
│   ├── .env
│   ├── requirements.txt
│   ├── signal.db
│   └── README.md
│
├── frontend/
│   └── README.md
│
└── README.md
```

The backend has its own detailed documentation covering its architecture, database, APIs, design patterns, and WebSocket implementation.

See:

```text
backend/README.md
```

---

# 4. High-Level Architecture

```text
                         ┌─────────────────────┐
                         │       User          │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      Next.js        │
                         │      Frontend       │
                         └───────┬─────┬───────┘
                                 │     │
                         HTTP API│     │WebSocket
                                 │     │
                                 ▼     ▼
                         ┌─────────────────────┐
                         │      FastAPI        │
                         │      Backend        │
                         └──────────┬──────────┘
                                    │
                     ┌──────────────┼──────────────┐
                     │              │              │
                     ▼              ▼              ▼
                Services      WebSocket       Repositories
                     │          Manager            │
                     │              │              │
                     └──────────────┼──────────────┘
                                    │
                                    ▼
                              ┌───────────┐
                              │  SQLite   │
                              └───────────┘
```

---

# 5. Backend Architecture

The backend follows a layered architecture based on separation of concerns.

```text
Router
   │
   ▼
Service
   │
   ▼
Strategy / Factory
   │
   ▼
Repository
   │
   ▼
Database
```

Real-time communication uses an event-based architecture:

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
    ├──────► Sender
    │
    └──────► Receiver
```

---

# 6. Design Principles

The project follows established software engineering principles rather than putting all application logic into route handlers.

### SOLID

- **Single Responsibility** — each layer has a focused responsibility
- **Open/Closed** — new message types can be introduced through strategies
- **Liskov Substitution** — messaging strategies follow a common abstraction
- **Interface Segregation** — components expose only the behavior they need
- **Dependency Inversion** — business logic is separated from infrastructure concerns

### Design Patterns

The backend currently uses:

- Repository Pattern
- Service Layer Pattern
- Strategy Pattern
- Factory Pattern
- Observer / Pub-Sub Pattern
- Dependency Injection

The architecture is intentionally kept practical for the scope of the assignment rather than introducing unnecessary abstractions.

---

# 7. Core Features

## Authentication

Users can:

- Register
- Request an OTP
- Verify an OTP
- Receive a JWT access token
- Access protected resources using the token

Development OTP:

```text
123456
```

---

## Contacts

Users can:

- Add contacts
- View contacts
- Search users
- Remove contacts

Contacts are represented as a one-way relationship:

```text
User A
  │
  └──► User B
```

---

## Direct Messaging

Users can:

- Send direct messages
- Retrieve conversation history
- Persist messages in SQLite
- Track message status

Message lifecycle:

```text
SENT → DELIVERED → READ
```

---

## Real-Time Messaging

WebSockets provide real-time communication between connected clients.

Example:

```text
User A
  │
  │ WebSocket
  ▼
Backend
  │
  ├── Persist message
  │
  └── Publish event
        │
        ▼
   WebSocket Manager
        │
        ▼
     User B
```

---

## Groups

Planned group functionality includes:

- Create groups
- Add members
- Remove members
- Assign administrators
- View members
- Send group messages
- Persist group membership

---

# 8. Database

SQLite is currently used for persistence.

Current entities:

```text
User
Contact
Message
```

Planned entities:

```text
Group
GroupMember
```

Conceptually:

```text
User
 │
 ├────────── Contact
 │
 ├────────── Message
 │
 └────────── GroupMember
                    │
                    ▼
                  Group
```

---

# 9. Current Implementation Status

### Backend

- [x] Project foundation
- [x] SQLite configuration
- [x] SQLAlchemy setup
- [x] User model
- [x] Registration
- [x] Mock OTP authentication
- [x] JWT authentication
- [x] Current-user authentication
- [x] Contact management
- [x] Contact search
- [x] Direct messaging
- [x] Message persistence
- [x] Message status API
- [x] WebSocket authentication
- [x] WebSocket connection manager
- [x] Real-time direct messaging
- [x] Message event publishing

### In Progress / Upcoming

- [ ] Automatic delivery receipts
- [ ] Read receipts through WebSockets
- [ ] Online/offline presence
- [ ] Typing indicators
- [ ] Group model
- [ ] Group membership
- [ ] Group messaging
- [ ] Group administration
- [ ] Frontend implementation
- [ ] Frontend/backend integration
- [ ] Automated tests
- [ ] Deployment

---

# 10. Frontend

The frontend will be implemented using:

```text
Next.js
TypeScript
React
WebSockets
```

The interface will follow the design language of Signal while remaining an independent implementation.

Planned screens:

```text
Authentication
    │
    ├── Registration
    └── Login / OTP
             │
             ▼
        Main Application
             │
       ┌─────┴─────┐
       │           │
    Contacts    Conversations
                     │
              ┌──────┴──────┐
              │             │
           Direct          Group
           Chat             Chat
```

---

# 11. Local Development

## Prerequisites

Install:

- Python 3.11+
- Node.js 18+
- npm
- Git