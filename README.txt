# Reminder Service

A ZeroMQ-based reminder microservice for the Workout app that allows the user to create, retrieve and check for reminders by sending and receiving JSON messages over a ZMQ socket

# Requirements

- Python 3
- pyzmq

# Run

python service_reminder.py

# Communication Contract

Port    tcp://localhost:5555
Pattern ZMQ REQ/REP 
Format  JSON  

# Connecting to the Service

import zmq
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

# Requesting Data

socket.send_json({
    "action": "create",
    "userId": "abc",
    "title": "Morning Run",
    "datetime": "2025-06-01 07:00"
})

*Example request:

socket.send_json({
    "action": "get",
    "userId": "abc"
})

# Receiving Data

After every send_json() call, call recv_json() to receive the response

*Example response:

{
    "status": "success",
    "reminder": {
        "id": 1,
        "userId": "abc",
        "title": "Morning Run",
        "datetime": "2025-06-01 07:00",
        "created_at": "2025-05-30 14:32:00"
    }
}

# UML Sequence Diagram

UML diagram attached for reference