from flask import Blueprint, request, jsonify
from models import Event, Booking
import storage

api = Blueprint("api", __name__)

@api.route("/events", methods=["POST"])
def create_event():
    data = request.json

    event = Event(
        name=data["name"],
        date_time=data["date_time"],
        venue=data["venue"],
        total_seats=data["total_seats"]
    )

    storage.add_event(event)

    return jsonify({"event_id": event.id}), 201


@api.route("/events/<event_id>/seats", methods=["GET"])
def seat_availability(event_id):
    event = storage.get_event(event_id)
    if not event:
        return jsonify({"error": "event not found"}), 404

    available = event.total_seats - len(event.booked_seats)

    return jsonify({
        "total_seats": event.total_seats,
        "booked_seats": len(event.booked_seats),
        "available_seats": available
    })


@api.route("/bookings", methods=["POST"])
def create_booking():
    data = request.json
    event = storage.get_event(data["event_id"])

    if not event:
        return jsonify({"error": "event not found"}), 404

    requested_seats = set(data["seats"])

    if requested_seats & event.booked_seats:
        return jsonify({"error": "one or more seats already booked"}), 400

    event.booked_seats.update(requested_seats)

    booking = Booking(event.id, list(requested_seats))
    storage.add_booking(booking)

    return jsonify({
        "booking_id": booking.id,
        "status": booking.status
    }), 201
