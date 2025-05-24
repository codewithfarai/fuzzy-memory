import os

class Config:
    def __init__(self):
        """Base configuration variables."""
        # Default to test values if FLASK_ENV is 'testing'
        is_testing = os.environ.get('FLASK_ENV') == 'testing'
        
        # Secret key configuration
        self.SECRET_KEY = os.environ.get('SECRET_KEY')
        if not self.SECRET_KEY:
            if is_testing:
                self.SECRET_KEY = 'test-secret-key'
            else:
                raise ValueError("No SECRET_KEY set for Flask application. Did you follow the setup instructions?")

        # Database configuration
        self.SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
        if not self.SQLALCHEMY_DATABASE_URI:
            if is_testing:
                self.SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
            else:
                raise ValueError("No DATABASE_URL set for Flask application.")
        
        # Disable track modifications to save resources
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False
        
        # JWT configuration
        self.JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', self.SECRET_KEY)

class TestConfig:
    """Test configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SECRET_KEY = 'test-secret-key'
    JWT_SECRET_KEY = 'test-jwt-secret-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
