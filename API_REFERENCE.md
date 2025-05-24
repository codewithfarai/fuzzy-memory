# Booking Service API Reference

## Quick Start

### 1. Create a Provider (Manual - via SQL)
```sql
INSERT INTO provider (name, email) VALUES ('Dr. Smith', 'dr.smith@example.com');
```

### 2. Create a Booking
```bash
curl -X POST http://localhost:5000/api/v1/bookings \
  -H "Content-Type: application/json" \
  -d '{
    "provider_id": 1,
    "date": "2024-12-25",
    "time": "14:30"
  }'
```

## API Endpoints

### POST /api/v1/bookings
Create a new booking for a provider.

#### Request
- **Method**: POST
- **URL**: `/api/v1/bookings`
- **Headers**: `Content-Type: application/json`
- **Body**:
  ```json
  {
    "provider_id": integer (required),
    "date": "YYYY-MM-DD" (required),
    "time": "HH:MM" (required)
  }
  ```

#### Responses

##### Success (201 Created)
```json
{
  "id": 1,
  "provider_id": 1,
  "date": "2024-12-25",
  "time": "14:30:00",
  "created_at": "2024-01-15T10:30:00"
}
```

##### Error Responses

**400 Bad Request** - Missing required fields
```json
{
  "error": "Missing required fields: provider_id, date, time"
}
```

**404 Not Found** - Provider doesn't exist
```json
{
  "error": "Provider not found"
}
```

**409 Conflict** - Time slot already booked
```json
{
  "error": "This time slot is already booked"
}
```

## Examples

### Using cURL

#### Create a booking
```bash
curl -X POST http://localhost:5000/api/v1/bookings \
  -H "Content-Type: application/json" \
  -d '{
    "provider_id": 1,
    "date": "2024-12-25",
    "time": "14:30"
  }'
```

### Using Python Requests

```python
import requests

url = "http://localhost:5000/api/v1/bookings"
data = {
    "provider_id": 1,
    "date": "2024-12-25",
    "time": "14:30"
}

response = requests.post(url, json=data)
print(response.json())
```

### Using JavaScript Fetch

```javascript
fetch('http://localhost:5000/api/v1/bookings', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    provider_id: 1,
    date: '2024-12-25',
    time: '14:30'
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

## Data Formats

### Date Format
- Format: `YYYY-MM-DD`
- Example: `2024-12-25`

### Time Format
- Format: `HH:MM` (24-hour format)
- Example: `14:30` for 2:30 PM
- Stored as: `HH:MM:SS` in response

### Datetime Format
- ISO 8601 format in UTC
- Example: `2024-01-15T10:30:00`

## Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Invalid request data |
| 404 | Not Found | Resource not found |
| 409 | Conflict | Resource conflict (e.g., double booking) |
| 500 | Internal Server Error | Server error |

## Testing the API

### 1. Start the server
```bash
poetry run flask run
```

### 2. Create test data
```sql
-- Connect to your database and run:
INSERT INTO provider (name, email) VALUES 
  ('Dr. Smith', 'dr.smith@example.com'),
  ('Dr. Jones', 'dr.jones@example.com');
```

### 3. Test endpoints
```bash
# Test successful booking
curl -X POST http://localhost:5000/api/v1/bookings \
  -H "Content-Type: application/json" \
  -d '{"provider_id": 1, "date": "2024-12-25", "time": "14:30"}'

# Test conflict (run same request again)
curl -X POST http://localhost:5000/api/v1/bookings \
  -H "Content-Type: application/json" \
  -d '{"provider_id": 1, "date": "2024-12-25", "time": "14:30"}'

# Test missing fields
curl -X POST http://localhost:5000/api/v1/bookings \
  -H "Content-Type: application/json" \
  -d '{"provider_id": 1}'

# Test invalid provider
curl -X POST http://localhost:5000/api/v1/bookings \
  -H "Content-Type: application/json" \
  -d '{"provider_id": 999, "date": "2024-12-25", "time": "14:30"}'
```

## Future Endpoints (Planned)

### GET /api/v1/bookings
Retrieve bookings with optional filters.

**Query Parameters**:
- `provider_id`: Filter by provider
- `date`: Filter by date
- `start_date` & `end_date`: Date range filter

### PUT /api/v1/bookings/{id}
Update an existing booking.

### DELETE /api/v1/bookings/{id}
Cancel a booking.

### GET /api/v1/providers/{id}/availability
Check available time slots for a provider. 