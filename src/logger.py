import csv
import os
from datetime import datetime

def log_event(username, role, action, status):
    """Write a usage log entry to Data/usage_log.csv."""
    log_path = "Data/usage_log.csv"
    file_exists = os.path.isfile(log_path)

    with open(log_path, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["timestamp", "username", "role", "action", "status"])

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([timestamp, username, role, action, status])
