import zmq
import json
from datetime import datetime
import threading
import time

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

reminders = []
triggered_reminders = set()

def check_reminders():
    """Background thread that checks for due reminders"""
    while True:
        current_time = datetime.now()
        for reminder in reminders:
            reminder_id = reminder["id"]
            if reminder_id in triggered_reminders:
                continue
            try:
                reminder_time = datetime.strptime(reminder["datetime"], "%Y-%m-%d %H:%M")
                time_diff = (current_time - reminder_time).total_seconds()
                if 0 <= time_diff <= 60:
                    print("\n" + "=" * 60)
                    print("⏰ REMINDER ALERT! ⏰")
                    print("=" * 60)
                    print(f"User: {reminder['userId']}")
                    print(f"Title: {reminder['title']}")
                    print(f"Scheduled Time: {reminder['datetime']}")
                    print("=" * 60 + "\n")
                    triggered_reminders.add(reminder_id)
            except ValueError:
                pass
        time.sleep(30)

checker_thread = threading.Thread(target=check_reminders, daemon=True)
checker_thread.start()

print("Reminder Service running...")
print("Checking for due reminders every 30 seconds...")

while True:
    request = socket.recv_json()
    action = request.get("action")
    if action == "create":
        reminder = {
            "id": len(reminders) + 1,
            "userId": request["userId"],
            "title": request["title"],
            "datetime": request["datetime"],
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        reminders.append(reminder)
        socket.send_json({"status": "success", "reminder": reminder})
    elif action == "get":
        user_id = request["userId"]
        user_reminders = [r for r in reminders if r["userId"] == user_id]
        socket.send_json({"status": "success", "reminders": user_reminders})
    elif action == "check_due":
        user_id = request["userId"]
        current_time = datetime.now()
        due_reminders = []
        for reminder in reminders:
            if reminder["userId"] != user_id:
                continue
            try:
                reminder_time = datetime.strptime(reminder["datetime"], "%Y-%m-%d %H:%M")
                time_diff = (current_time - reminder_time).total_seconds()
                if 0 <= time_diff <= 300:
                    due_reminders.append(reminder)
            except ValueError:
                pass
        socket.send_json({"status": "success", "due_reminders": due_reminders})
    else:
        socket.send_json({"status": "error", "message": "Invalid action"})
