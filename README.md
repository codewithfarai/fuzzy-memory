# Booking Service API

A RESTful API for managing bookings and providers built with Flask and SQLAlchemy.

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Database Models](#database-models)
- [Development](#development)
- [Troubleshooting](#troubleshooting)

## Features

- RESTful API for booking management
- Provider and booking relationship management
- Input validation for bookings
- Conflict detection for double bookings
- SQLite for testing, PostgreSQL for production
- Comprehensive test suite
- Environment-based configuration

## Tech Stack

- **Framework**: Flask 3.0.0
- **Database**: PostgreSQL (production), SQLite (testing)
- **ORM**: SQLAlchemy via Flask-SQLAlchemy
- **Testing**: pytest, pytest-flask
- **Package Management**: Poetry
- **Python**: 3.8+

## Project Structure

```
booking_service/
├── booking_service/
│   ├── __init__.py
│   ├── app.py              # Flask application factory
│   ├── flask_config.py     # Configuration classes
│   ├── extensions.py       # Flask extensions
│   ├── models.py          # Database models
│   └── routes.py          # API endpoints
├── tests/
│   ├── __init__.py
│   ├── conftest.py        # pytest fixtures
│   └── test_routes.py     # API tests
├── .env                   # Environment variables (create this)
├── .env.example          # Example environment variables
├── pyproject.toml        # Poetry configuration
├── poetry.lock           # Locked dependencies
└── README.md            # This file
```

## Installation

### Prerequisites

- Python 3.8 or higher
- Poetry (for dependency management)
- PostgreSQL (for production)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd booking_service
   ```

2. **Install dependencies using Poetry**
   ```bash
   poetry install
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your configuration:
   ```
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=postgresql://username:password@localhost:5432/booking_db
   FLASK_ENV=development
   ```

4. **Set up the database**
   
   For PostgreSQL:
   ```sql
   CREATE DATABASE booking_db;
   CREATE USER your_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE booking_db TO your_user;
   ```

## Configuration

The application uses different configuration classes for different environments:

- `Config`: Base configuration with environment variable support
- `TestConfig`: Test configuration using SQLite in-memory database

Configuration is managed in `booking_service/flask_config.py`.

### Environment Variables

Required environment variables for production:
- `SECRET_KEY`: Flask secret key for session management
- `DATABASE_URL`: PostgreSQL connection string
- `FLASK_ENV`: Environment (development/production/testing)

## Running the Application

### Development Server

```bash
# Activate the virtual environment
poetry shell

# Run the Flask development server
flask run
```

The API will be available at `http://localhost:5000`.

### Production

For production deployment, use a WSGI server like Gunicorn:

```bash
poetry add gunicorn
gunicorn booking_service.app:create_app()
```

## API Documentation

### Base URL
All endpoints are prefixed with `/api/v1`

### Endpoints

#### Create Booking
Creates a new booking for a provider.

**Endpoint:** `POST /api/v1/bookings`

**Request Body:**
```json
{
    "provider_id": 1,
    "date": "2024-12-25",
    "time": "14:30"
}
```

**Response (Success - 201):**
```json
{
    "id": 1,
    "provider_id": 1,
    "date": "2024-12-25",
    "time": "14:30:00",
    "created_at": "2024-01-15T10:30:00"
}
```

**Response (Conflict - 409):**
```json
{
    "error": "This time slot is already booked"
}
```

**Response (Bad Request - 400):**
```json
{
    "error": "Missing required fields: provider_id, date, time"
}
```

**Response (Not Found - 404):**
```json
{
    "error": "Provider not found"
}
```

### Retrieve Bookings (Future Enhancement)
*Note: This endpoint is mentioned in requirements but not yet implemented*

**Endpoint:** `GET /api/v1/bookings`

## Testing

The project includes comprehensive tests for all endpoints.

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=booking_service

# Run tests with verbose output
poetry run pytest -v
```

### Test Configuration

Tests use SQLite in-memory database to avoid PostgreSQL dependency. Configuration is in `tests/conftest.py`.

### Test Coverage

The test suite covers:
- Successful booking creation
- Conflict detection for double bookings
- Validation of required fields
- Provider existence validation

## Database Models

### Provider Model
```python
class Provider(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    bookings = db.relationship('Booking', backref='provider', lazy=True)
```

### Booking Model
```python
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

## Development

### Setting up Development Environment

1. **Use virtual environment**
   ```bash
   poetry shell
   ```

2. **Install development dependencies**
   ```bash
   poetry install --with dev
   ```

3. **Create test database**
   ```sql
   CREATE DATABASE test_db;
   CREATE USER test WITH PASSWORD 'test';
   GRANT ALL PRIVILEGES ON DATABASE test_db TO test;
   ```

### Code Style

Follow PEP 8 guidelines for Python code style.

### Adding New Features

1. Create feature branch
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Implement feature with tests
3. Run tests to ensure nothing breaks
4. Submit pull request

## Troubleshooting

### Common Issues

#### ImportError: DLL load failed while importing _psycopg
**Solution**: This is a Windows-specific issue. The tests are configured to use SQLite instead of PostgreSQL to avoid this.

#### Connection refused to PostgreSQL
**Solution**: 
- Ensure PostgreSQL is installed and running
- Check your DATABASE_URL in .env
- Verify PostgreSQL is listening on the correct port (default: 5432)

#### Tests failing with database errors
**Solution**: Tests should use SQLite automatically. Ensure you're running tests with `poetry run pytest`.

### Windows-Specific Setup

1. **PostgreSQL Installation**
   - Download from https://www.postgresql.org/download/windows/
   - Add PostgreSQL bin directory to PATH
   - Default location: `C:\Program Files\PostgreSQL\[version]\bin`

2. **Alternative: Use WSL2**
   - Install WSL2 with Ubuntu
   - Install PostgreSQL in WSL2
   - Run the application in WSL2 environment

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
- Create an issue in the GitHub repository
- Check existing issues for solutions
- Refer to Flask documentation: https://flask.palletsprojects.com/
- SQLAlchemy documentation: https://www.sqlalchemy.org/

## Roadmap

- [ ] Implement GET /api/v1/bookings endpoint
- [ ] Add authentication and authorization
- [ ] Implement booking updates and deletions
- [ ] Add pagination for booking listings
- [ ] Add booking time slot availability checker
- [ ] Implement email notifications
- [ ] Add API rate limiting
- [ ] Add comprehensive logging
- [ ] Create OpenAPI/Swagger documentation
- [ ] Add Docker support
