from datetime import datetime, timedelta
from uuid import UUID
from flask import Blueprint, request, jsonify
from sqlalchemy import and_

from booking_service.extensions import db
from booking_service.models.booking import Booking
from booking_service.models.provider import Provider

bp = Blueprint('bookings', __name__)

@bp.route('/bookings', methods=['POST'])
def create_booking():
    """Create a new booking."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['provider_id', 'date', 'time']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400

        # Get client_id from JWT token (assumed to be in request context)
        client_id = request.headers.get('X-Client-ID')
        if not client_id:
            return jsonify({'error': 'Client ID is required'}), 401

        try:
            provider_id = UUID(data['provider_id'])
        except ValueError:
            return jsonify({'error': 'Invalid provider_id format'}), 400

        # Validate provider exists
        provider = Provider.query.get(provider_id)
        if not provider:
            return jsonify({'error': 'Provider not found'}), 404

        # Parse and validate datetime
        try:
            date_str = data['date']
            time_str = data['time']
            start_time = datetime.fromisoformat(f"{date_str}T{time_str}")
            # Assuming 1-hour appointments
            end_time = datetime.fromisoformat(f"{date_str}T{time_str}") + timedelta(hours=1)
        except ValueError:
            return jsonify({'error': 'Invalid date or time format. Use ISO format'}), 400

        # Check for overlapping bookings
        overlapping = Booking.query.filter(
            and_(
                Booking.provider_id == provider_id,
                Booking.start_time < end_time,
                Booking.end_time > start_time
            )
        ).first()

        if overlapping:
            return jsonify({
                'error': 'Time slot is already booked',
                'existing_booking': overlapping.to_dict()
            }), 400

        # Create booking
        booking = Booking(
            client_id=client_id,
            provider_id=provider_id,
            start_time=start_time,
            end_time=end_time
        )

        db.session.add(booking)
        db.session.commit()

        return jsonify({
            'message': 'Booking created successfully',
            'booking': booking.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 