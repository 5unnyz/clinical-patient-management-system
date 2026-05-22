import tkinter as tk
from tkinter import messagebox
import csv
import datetime
import os

class LoginWindow:
    def __init__(self, root, on_login_success):
        self.root = root
        self.root.title("Hospital Login")
        self.on_login_success = on_login_success

        # UI layout
        tk.Label(root, text="Username:").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(root, text="Password:").grid(row=1, column=0, padx=10, pady=10)

        self.username_entry = tk.Entry(root)
        self.password_entry = tk.Entry(root, show="*")

        self.username_entry.grid(row=0, column=1)
        self.password_entry.grid(row=1, column=1)

        tk.Button(root, text="Login", command=self.validate_login).grid(row=2, column=0, columnspan=2, pady=10)

        # Ensure usage log exists
        os.makedirs("output", exist_ok=True)
        self.usage_log_path = os.path.join("output", "usage_log.csv")

        if not os.path.exists(self.usage_log_path):
            with open(self.usage_log_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["username", "role", "login_time", "status", "actions"])

    def validate_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        role = self.check_credentials(username, password)

        login_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if role is None:
            messagebox.showerror("Login Failed", "Invalid username or password.")
            self.log_usage(username, "N/A", login_time, "FAILED", "")
            return

        # Successful login
        self.log_usage(username, role, login_time, "SUCCESS", "")
        self.on_login_success(username, role)
        self.root.destroy()

    def check_credentials(self, username, password):
        with open("Data/credentials.csv", "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["username"] == username and row["password"] == password:
                    return row["role"]
        return None

    def log_usage(self, username, role, login_time, status, actions):
        with open(self.usage_log_path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([username, role, login_time, status, actions])
