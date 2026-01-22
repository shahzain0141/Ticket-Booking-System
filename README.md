# Ticket Booking System

A lightweight event ticketing backend service that handles event creation and seat bookings. Built with Flask and designed to be simple, fast, and easy to understand.


# Install dependencies:
   pip install flask


# Running the Service
**Direct Run:**
# Run in test mode(to test without HTTP requests):

python app.py test

 
**# IF Use API:**
# Start the Flask server:
python app.py

The service will start on `http://127.0.0.1:5000`

## How It Works

### High-Level Design

This is a straightforward ticketing backend where users can create events and book seats. Everything runs in memory, which means the system is fast but loses all data when restarted. Think of it as a prototype or learning tool rather than a production system.

The system has three main layers:
Data Models: Define what an Event and Booking look like
Storage Layer: Keeps events and bookings in Python dictionaries
API Routes: Expose HTTP endpoints so clients can interact with the system

### Main Components

Event Model
Stores event details like name, date, venue, and total seats
Tracks which seats have been booked using a set (for fast lookups)
Gets a unique ID when created

Booking Model
Represents a customer's booking for specific seats
Links to an event through the event ID
Records when the booking was created

Storage Module
Simple in-memory storage using dictionaries
Keys are event IDs or booking IDs, values are the objects
All data lives in RAM and disappears when the app stops

Flask Routes
`POST /events` - Create a new event
`GET /events/{event_id}/seats` - Check how many seats are available
`POST /bookings` - Book seats for an event

# Using the API

# Create an Event

bash
curl -X POST http://localhost:5000/events \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Summer Concert",
    "date_time": "2024-06-15 19:00",
    "venue": "Central Park",
    "total_seats": 500
  }'


Response:
json
{
  "event_id": "f1d69c4a-b6c2-49bc-bd12-03979bc14f11"
}


# Check Available Seats
use the above event ID:
bash
curl http://localhost:5000/events/f1d69c4a-b6c2-49bc-bd12-03979bc14f11/seats


Response:
json
{
  "total_seats": 500,
  "booked_seats": 0,
  "available_seats": 500
}


# Book Seats
use the above event ID:
bash
curl -X POST http://localhost:5000/bookings \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": "f1d69c4a-b6c2-49bc-bd12-03979bc14f11",
    "seats": [1, 2, 3, 4, 5]
  }'


Response:
json
{
  "booking_id": "a8f2c1d0-9e8b-4c3a-7f5e-2b9d1a0c3e7f",
  "status": "confirmed"
}


# Design Decisions

Why use a set for tracking booked seats?
Sets in Python are optimized for checking if something exists. When we need to verify that seats [1, 2, 3] aren't already booked, a set lets us do this instantly instead of looping through a list. This scales well even with thousands of bookings.

Why use UUIDs for IDs?
UUIDs guarantee uniqueness without needing a database. Each event and booking gets its own random identifier that won't collide with others, even if the system is distributed across multiple instances.

Why keep everything in memory?
For a prototype or learning project, in-memory storage is perfect. It's incredibly fast, requires zero setup (no database), and the code is easy to understand. The tradeoff is that data disappears when the app restarts.

Why no external dependencies?
We only use Flask, which is lightweight and standard. No queuing systems, caching layers, or complex frameworks. This keeps the codebase small and easy to debug.

# Known Limitations

Race Conditions
If two customers try to book the same seat at the exact same millisecond, both requests might succeed. There's no locking mechanism to prevent this. In a real system, you'd need to handle concurrent requests carefully.

No Authentication or Authorization
Anyone can create events or bookings. There's no concept of event ownership or user accounts. You could add this later if needed.

No Seat Locking
When a customer starts booking, we don't temporarily reserve their seats. If they abandon their booking halfway through, those seats remain available to others. A production system would lock seats during the booking process.

Data Loss on Restart
Everything is stored in RAM. If the server crashes or restarts, all events and bookings are lost. For a real ticketing system, you'd need a database like PostgreSQL or MongoDB.

No Validation
The API doesn't check if dates are in the future, if seat numbers make sense, or if required fields are missing. It trusts that input is well-formed.

Single-Server Only
This works on one machine only. If you wanted to run multiple instances for high availability, the in-memory storage would create separate databases on each instance.

# What We'd Improve with More Time

Add a Real Database
Replace the in-memory dictionaries with PostgreSQL or MongoDB. This gives us persistence, scalability, and the ability to run multiple server instances.

Implement Seat Locking
When a customer starts their checkout, lock those seats for 5-10 minutes. If they don't complete the booking, release the lock automatically. This prevents overbooking.

Support Booking Cancellations
Let customers cancel bookings and get refunds. This means removing bookings from storage and freeing up seats.

Add Better Validation
Check that dates are in the future
Validate that seat numbers are within the event's range
Ensure seat arrays don't have duplicates
Return helpful error messages when validation fails

Write Comprehensive Tests
Add unit tests for the models, integration tests for the API routes, and load tests to see how many bookings we can handle per second.

Add Authentication
Implement user accounts so customers can see their own bookings. Require API keys or tokens for sensitive operations.

Handle Concurrency Properly
Add database-level constraints and transaction support to handle multiple simultaneous bookings safely.

Improve API Design
Add pagination for listing events
Support filtering (e.g., events by date range or venue)
Add endpoints to get booking details
Include more detailed error messages

Add Logging and Monitoring
Track requests, errors, and performance metrics so we can debug problems and spot bottlenecks.

Deploy Properly
Put the app behind a production WSGI server (like Gunicorn), add environment variables for configuration, and containerize with Docker for easy deployment.
