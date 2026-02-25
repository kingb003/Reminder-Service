import zmq
import time
from datetime import timedelta, datetime

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

user_id = 1
title = "Test Reminder"
t = datetime.now() + timedelta(seconds=30)

socket.send_json({
    "action": "create",
    "userId": user_id,
    "title": title,
    "datetime": t.strftime("%Y-%m-%d %H:%M") # This MUST only be to minute-level precision
})

message = socket.recv_json()
if message.get('status') == 'success':
    reminder = message.get('reminder')
    print(f"=== Reminder Created Successfully: {reminder}")

socket.send_json({
    "action": "get",
    "userId": user_id
})

message = socket.recv_json()
if message.get('status') == 'success':
    reminders = message.get("reminders")
    for r in reminders:
        if r == reminder:
            print(f"=== Reminder {reminder["id"]} Is Valid")

b = True
while b:
    socket.send_json({
        "action": "check_due",
        "userId": user_id
    })

    message = socket.recv_json()
    if message.get('status') == 'success':
        reminders = message.get("due_reminders")
        for r in reminders:
            if r['id'] == reminder['id']:
                print(f"=== Reminder {reminder["id"]} has passed!")
                b = False
        if len(reminders) == 0:
            print("No Reminders have passed")
    time.sleep(10)

socket.close()