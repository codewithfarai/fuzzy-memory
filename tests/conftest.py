import os
import pytest
from booking_service.app import create_app
from booking_service.flask_config import TestConfig
from booking_service.extensions import db

# Set test environment
os.environ['FLASK_ENV'] = 'testing'

@pytest.fixture(scope='session')
def app():
    """Create and configure a Flask app for testing."""
    app = create_app(TestConfig)
    app.config['TESTING'] = True

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='function')
def client(app):
    """Create a test client."""
    return app.test_client()

@pytest.fixture(scope='function')
def _db(app):
    """Provide the transactional fixtures with access to the database."""
    with app.app_context():
        yield db 