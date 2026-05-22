import tkinter as tk
from tkinter import messagebox
from src.logger import log_event

class MenuWindow:
    def __init__(self, root, username, role):
        self.root = root
        self.username = username
        self.role = role

        self.root.title(f"Welcome, {username} ({role})")

        tk.Label(root, text=f"Logged in as: {username}", font=("Arial", 12)).pack(pady=10)
        tk.Label(root, text=f"Role: {role}", font=("Arial", 12, "bold")).pack(pady=5)

        if role in ["nurse", "clinician"]:
            self.build_clinician_menu()
        elif role == "admin":
            self.build_admin_menu()
        elif role == "management":
            self.build_management_menu()
        else:
            messagebox.showerror("Error", "Unknown role.")
            root.destroy()

    # ============================================================
    # CLINICIAN / NURSE MENU
    # ============================================================
    def build_clinician_menu(self):
        tk.Button(self.root, text="Retrieve Patient", width=25,
                  command=self.open_retrieve_patient).pack(pady=5)

        tk.Button(self.root, text="Add Patient", width=25,
                  command=self.open_add_patient).pack(pady=5)

        tk.Button(self.root, text="Remove Patient", width=25,
                  command=self.open_remove_patient).pack(pady=5)

        tk.Button(self.root, text="Count Visits", width=25,
                  command=self.open_count_visits).pack(pady=5)

        tk.Button(self.root, text="View Note", width=25,
                  command=self.open_view_note).pack(pady=5)

        tk.Button(self.root, text="Exit", width=25,
                  command=self.exit_app).pack(pady=10)

    # ============================================================
    # ADMIN MENU
    # ============================================================
    def build_admin_menu(self):
        tk.Button(self.root, text="Count Encounters Per Patient", width=30,
                  command=self.open_count_encounters_per_patient).pack(pady=5)

        tk.Button(self.root, text="Count Encounters by Department", width=30,
                  command=self.open_count_encounters_by_department).pack(pady=5)

        tk.Button(self.root, text="Monitor Provider Workload", width=30,
                  command=self.open_monitor_provider_workload).pack(pady=5)

        tk.Button(self.root, text="Exit", width=30,
                  command=self.exit_app).pack(pady=10)

    # ============================================================
    # MANAGEMENT MENU
    # ============================================================
    def build_management_menu(self):
        tk.Button(self.root, text="Monitor Provider Workload", width=30,
                  command=self.open_monitor_provider_workload).pack(pady=5)

        tk.Button(self.root, text="Exit", width=30,
                  command=self.exit_app).pack(pady=10)

    # ============================================================
    # ACTION WINDOWS
    # ============================================================
    def open_retrieve_patient(self):
        from src.gui_actions import RetrievePatientWindow
        log_event(self.username, self.role, "Open RetrievePatientWindow", "success")
        RetrievePatientWindow(self.root, self.username, self.role)

    def open_add_patient(self):
        from src.gui_actions import AddPatientWindow
        log_event(self.username, self.role, "Open AddPatientWindow", "success")
        AddPatientWindow(self.root, self.username, self.role)

    def open_remove_patient(self):
        from src.gui_actions import RemovePatientWindow
        log_event(self.username, self.role, "Open RemovePatientWindow", "success")
        RemovePatientWindow(self.root, self.username, self.role)

    def open_count_visits(self):
        from src.gui_actions import CountVisitsWindow
        log_event(self.username, self.role, "Open CountVisitsWindow", "success")
        CountVisitsWindow(self.root, self.username, self.role)

    def open_view_note(self):
        from src.gui_actions import ViewNoteWindow
        log_event(self.username, self.role, "Open ViewNoteWindow", "success")
        ViewNoteWindow(self.root, self.username, self.role)

    def open_count_encounters_per_patient(self):
        from src.gui_actions import CountEncountersPerPatientWindow
        log_event(self.username, self.role, "Open CountEncountersPerPatientWindow", "success")
        CountEncountersPerPatientWindow(self.root, self.username, self.role)

    def open_count_encounters_by_department(self):
        from src.gui_actions import CountEncountersByDepartmentWindow
        log_event(self.username, self.role, "Open CountEncountersByDepartmentWindow", "success")
        CountEncountersByDepartmentWindow(self.root, self.username, self.role)

    def open_monitor_provider_workload(self):
        from src.gui_actions import MonitorProviderWorkloadWindow
        log_event(self.username, self.role, "Open MonitorProviderWorkloadWindow", "success")
        MonitorProviderWorkloadWindow(self.root, self.username, self.role)

    def exit_app(self):
        log_event(self.username, self.role, "Exit", "success")
        self.root.destroy()
