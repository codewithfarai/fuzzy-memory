from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from booking_service.extensions import db

class Booking(db.Model):
    """Model for storing booking information."""
    __tablename__ = 'bookings'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    client_id = Column(String, nullable=False, index=True)
    provider_id = Column(UUID(as_uuid=True), ForeignKey('providers.id'), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    provider = relationship('Provider', back_populates='bookings')

    # Constraints
    __table_args__ = (
        CheckConstraint('start_time < end_time', name='check_start_before_end'),
    )

    def to_dict(self):
        """Convert booking to dictionary."""
        return {
            'id': str(self.id),
            'client_id': self.client_id,
            'provider_id': str(self.provider_id),
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 