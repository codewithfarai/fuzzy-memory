# ✂️ Booking Service – Developer Reference (Flask + Poetry)

## 🎯 Purpose

The **Booking Service** is a microservice responsible for managing the scheduling and coordination of appointments between clients and service providers (e.g., barbers). It handles appointment creation, modification, cancellations, and real-time availability.

---

## 🔧 Core Features

### 1. 📅 Booking Management
- **Create a Booking**  
  Client requests an appointment specifying provider, time, and optional notes.

- **Update a Booking**  
  Allows changes to time, notes, or status (e.g., confirmed, cancelled).

- **Cancel a Booking**  
  Cancels an existing appointment.

- **List Bookings**  
  Retrieve bookings by client, service provider, or timeframe.

---

### 2. 🕒 Provider Schedules
- Define provider availability (e.g., 9AM–5PM).
- Avoids double-booking based on existing entries.
- Optional support for breaks and blocked times.

---

### 3. 📈 Real-Time Availability
- Returns open time slots based on provider availability and current bookings.
- Optional: calculate estimated wait times for walk-ins.

---

### 4. 🔄 Integration Events
- Emits events to:
  - `auth-service` – to validate JWT tokens and identities.
  - `notification-service` – to send WhatsApp/SMS/email updates.
  - `analytics-service` – to track booking trends.

---

## 🧱 Tech Stack

| Layer             | Technology         |
|------------------|--------------------|
| Framework        | Flask              |
| ORM              | SQLAlchemy         |
| DB               | PostgreSQL         |
| Auth             | JWT (via auth-service) |
| Env Management   | `python-dotenv`    |
| Containerization | Docker             |
| Dependency Mgmt  | Poetry             |
| Testing          | Pytest + Flask     |

---


---

## 📦 Dependency Management (Poetry)

- Install packages with:

  ```bash
  poetry add <package-name>
  ```

- Development/testing dependencies:

  ```bash
  poetry add --group dev <package-name>
  ```

- Required dependencies:

  ```bash
  poetry add flask flask_sqlalchemy python-dotenv
  poetry add --group dev pytest pytest-flask
  ```

- Example `.env.example`:

  ```
  FLASK_ENV=development
  DATABASE_URL=postgresql://user:password@localhost:5432/booking_db
  SECRET_KEY=your-secret-key
  ```

---


---

## 🌐 API Endpoints (Example)

| Method | Endpoint              | Description                |
|--------|-----------------------|----------------------------|
| POST   | `/bookings`           | Create a new booking       |
| GET    | `/bookings`           | List bookings              |
| PUT    | `/bookings/<id>`      | Update a booking           |
| DELETE | `/bookings/<id>`      | Cancel a booking           |

---

## 🧪 Testing

- Tests live in `/tests` and use `pytest`.
- Mock database and JWT verification.
- Test cases should include:
  - ✅ Success
  - ⚠️ Edge case
  - ❌ Failure scenario

Run tests:
```bash
poetry run pytest
```

---

## 🧠 AI Assistant Behavior Rules (Cursor Context)

- Use **Flask** (not FastAPI).
- Use **Poetry** for dependencies.
- Add new packages via `poetry add`, not `pip`.
- Never create files >500 lines — modularize instead.
- Always write tests (success, failure, edge).
- Use PEP8 + `black` formatting.
- Use `.env` for secrets and config.
- Document with Google-style docstrings.
- Ask for clarification when uncertain — do not guess.
