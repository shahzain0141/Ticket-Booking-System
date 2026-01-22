from models import Event, Booking

events = {}
bookings = {}

def add_event(event):
    events[event.id] = event

def get_event(event_id):
    return events.get(event_id)

def add_booking(booking):
    bookings[booking.id] = booking
