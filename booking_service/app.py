from flask import Flask
from booking_service.flask_config import Config, TestConfig
from booking_service.extensions import db
from booking_service.routes import bp as bookings_bp
import os

def create_app(config_class=None):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Use provided config_class, or choose based on environment
    if config_class is not None:
        app.config.from_object(config_class)
    elif os.environ.get('FLASK_ENV') == 'testing':
        app.config.from_object(TestConfig())
    else:
        app.config.from_object(Config())

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(bookings_bp, url_prefix='/api/v1')

    # Create database tables
    with app.app_context():
        db.create_all()

    return app