import pytest
from datetime import datetime, timedelta
from uuid import uuid4
from booking_service.app import create_app
from booking_service.extensions import db
from booking_service.models.provider import Provider
from booking_service.models.booking import Booking

@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://test:test@localhost:5432/test_db'

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()

@pytest.fixture
def provider(_db):
    """Create a test provider."""
    provider = Provider(
        name='Test Provider',
        email='test@example.com',
        phone='1234567890'
    )
    _db.session.add(provider)
    _db.session.commit()
    return provider

def test_create_booking_success(client, provider):
    """Test successful booking creation."""
    # Prepare test data
    date = datetime.now().date().isoformat()
    time = '14:00:00'
    
    response = client.post(
        '/api/v1/bookings',
        json={
            'provider_id': str(provider.id),
            'date': date,
            'time': time
        },
        headers={'X-Client-ID': 'test-client'}
    )

    assert response.status_code == 201
    data = response.get_json()
    assert 'booking' in data
    assert data['booking']['provider_id'] == str(provider.id)
    assert data['booking']['client_id'] == 'test-client'

def test_create_booking_conflict(client, provider, _db):
    """Test booking conflict."""
    # Create an existing booking
    start_time = datetime.now().replace(hour=14, minute=0, second=0, microsecond=0)
    end_time = start_time + timedelta(hours=1)
    
    existing_booking = Booking(
        client_id='other-client',
        provider_id=provider.id,
        start_time=start_time,
        end_time=end_time
    )
    _db.session.add(existing_booking)
    _db.session.commit()

    # Try to book the same time slot
    response = client.post(
        '/api/v1/bookings',
        json={
            'provider_id': str(provider.id),
            'date': start_time.date().isoformat(),
            'time': '14:00:00'
        },
        headers={'X-Client-ID': 'test-client'}
    )

    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert 'Time slot is already booked' in data['error']

def test_create_booking_missing_fields(client):
    """Test booking creation with missing fields."""
    response = client.post(
        '/api/v1/bookings',
        json={},
        headers={'X-Client-ID': 'test-client'}
    )

    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert 'Missing required fields' in data['error'] 