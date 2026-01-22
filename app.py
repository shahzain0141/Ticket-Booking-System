from flask import Flask
from routes import api
from models import Event, Booking
import storage

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api)
    return app

def test_app():
    """Test the app without HTTP requests"""
    
    # Create an event
    event = Event(
        name="Concert",
        date_time="2024-02-15 19:00",
        venue="Stadium",
        total_seats=100
    )
    storage.add_event(event)
    print(f"Event created: {event.id}")
    print(f"  Name: {event.name}, Venue: {event.venue}, Seats: {event.total_seats}")
    
    # Check seat availability
    retrieved_event = storage.get_event(event.id)
    available = retrieved_event.total_seats - len(retrieved_event.booked_seats)
    print(f"\nSeat Availability:")
    print(f"  Total: {retrieved_event.total_seats}, Booked: {len(retrieved_event.booked_seats)}, Available: {available}")
    
    # Create a booking
    booking = Booking(event.id, [1, 2, 3])
    event.booked_seats.update([1, 2, 3])
    storage.add_booking(booking)
    print(f"\nBooking created: {booking.id}")
    print(f"  Seats: {booking.seats}, Status: {booking.status}")
    
    # Check seat availability after booking
    available = retrieved_event.total_seats - len(retrieved_event.booked_seats)
    print(f"\nUpdated Seat Availability:")
    print(f"  Total: {retrieved_event.total_seats}, Booked: {len(retrieved_event.booked_seats)}, Available: {available}")
    
    # Try booking already booked seats (should fail)
    print(f"\nTrying to book already booked seats [1, 2]:")
    if {1, 2} & event.booked_seats:
        print(" Error: Seats already booked!")
    
    # Try booking new seats
    print(f"\n Trying to book new seats [5, 6, 7]:")
    if not ({5, 6, 7} & event.booked_seats):
        booking2 = Booking(event.id, [5, 6, 7])
        event.booked_seats.update([5, 6, 7])
        storage.add_booking(booking2)
        print(f"  Booking successful: {booking2.id}")
        print(f"  Seats: {booking2.seats}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Run in test mode
        print("TESTING TICKET BOOKING SYSTEM")
        test_app()
        print("\n")
        print("TESTS COMPLETED")
    else:
        # Run Flask server
        app = create_app()
        print("Starting Flask server")
        app.run(debug=True)