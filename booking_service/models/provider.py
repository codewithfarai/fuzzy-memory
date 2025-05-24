from uuid import uuid4
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from booking_service.extensions import db

class Provider(db.Model):
    """Model for storing provider information."""
    __tablename__ = 'providers'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String)

    # Relationships
    bookings = relationship('Booking', back_populates='provider')

    def to_dict(self):
        """Convert provider to dictionary."""
        return {
            'id': str(self.id),
            'name': self.name,
            'email': self.email,
            'phone': self.phone
        } 