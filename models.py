from datetime import datetime
import uuid

class Event:
    def __init__(self, name, date_time, venue, total_seats):
        self.id = str(uuid.uuid4())
        self.name = name
        self.date_time = date_time
        self.venue = venue
        self.total_seats = total_seats
        self.booked_seats = set()

class Booking:
    def __init__(self, event_id, seats):
        self.id = str(uuid.uuid4())
        self.event_id = event_id
        self.seats = seats
        self.status = "confirmed"
        self.created_at = datetime.utcnow()
