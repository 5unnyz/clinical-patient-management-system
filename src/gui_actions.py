import tkinter as tk
from tkinter import messagebox
import csv
import os
from src.logger import log_event

# ============================================================
# ID NORMALIZATION HELPERS
# ============================================================

def normalize_id(pid):
    """Normalize to P# format (patients.csv, encounters.csv)."""
    pid = pid.upper().strip()
    if pid.startswith("P"):
        num = pid[1:]
        num = str(int(num))  # remove leading zeros
        return f"P{num}"
    return pid

def normalize_id_3(pid):
    """Normalize to P### format (notes.csv)."""
    pid = pid.upper().strip()
    if pid.startswith("P"):
        num = pid[1:]
        num = str(int(num))  # remove leading zeros
        return f"P{num.zfill(3)}"
    return pid


# ============================================================
# RETRIEVE PATIENT
# ============================================================
class RetrievePatientWindow:
    def __init__(self, root, username, role):
        self.root = tk.Toplevel(root)
        self.root.title("Retrieve Patient")
        self.username = username
        self.role = role

        tk.Label(self.root, text="Enter Patient ID:").grid(row=0, column=0, padx=10, pady=10)
        self.patient_id_entry = tk.Entry(self.root)
        self.patient_id_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Button(self.root, text="Search", command=self.search_patient).grid(row=1, column=0, columnspan=2, pady=10)

    def search_patient(self):
        raw_id = self.patient_id_entry.get().strip()
        patient_id = normalize_id(raw_id)

        if not raw_id:
            messagebox.showerror("Error", "Please enter a Patient ID.")
            log_event(self.username, self.role, "RetrievePatient (empty id)", "failed")
            return

        try:
            with open("Data/patients.csv", "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if normalize_id(row["patient_id"]) == patient_id:
                        info = (
                            f"Patient ID: {row['patient_id']}\n"
                            f"Age: {row['age']}\n"
                            f"Gender: {row['gender']}\n"
                            f"BMI: {row['bmi']}\n"
                            f"A1C: {row['a1c']}\n"
                            f"Systolic BP: {row['bp_sys']}\n"
                            f"Diastolic BP: {row['bp_dia']}\n"
                            f"Smoking: {row['smoking']}"
                        )
                        messagebox.showinfo("Patient Found", info)
                        log_event(self.username, self.role, f"RetrievePatient {raw_id}", "success")
                        return

            messagebox.showerror("Not Found", f"No patient found with ID {raw_id}")
            log_event(self.username, self.role, f"RetrievePatient {raw_id}", "failed")

        except FileNotFoundError:
            messagebox.showerror("Error", "patients.csv not found in Data folder.")
            log_event(self.username, self.role, "RetrievePatient (file missing)", "failed")


# ============================================================
# ADD PATIENT
# ============================================================
class AddPatientWindow:
    def __init__(self, root, username, role):
        self.root = tk.Toplevel(root)
        self.root.title("Add Patient")
        self.username = username
        self.role = role

        self.fields = [
            "patient_id", "age", "gender", "bmi",
            "a1c", "bp_sys", "bp_dia", "smoking"
        ]

        self.entries = {}

        for i, field in enumerate(self.fields):
            tk.Label(self.root, text=field + ":").grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(self.root)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[field] = entry

        tk.Button(self.root, text="Add Patient", command=self.add_patient).grid(row=len(self.fields), column=0, columnspan=2, pady=15)

    def add_patient(self):
        new_data = {field: self.entries[field].get().strip() for field in self.fields}

        if any(v == "" for v in new_data.values()):
            messagebox.showerror("Error", "All fields must be filled.")
            log_event(self.username, self.role, "AddPatient (missing fields)", "failed")
            return

        new_data["patient_id"] = normalize_id(new_data["patient_id"])

        try:
            with open("Data/patients.csv", "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if normalize_id(row["patient_id"]) == new_data["patient_id"]:
                        messagebox.showerror("Error", "Patient ID already exists.")
                        log_event(self.username, self.role, f"AddPatient {new_data['patient_id']} (duplicate)", "failed")
                        return
        except FileNotFoundError:
            messagebox.showerror("Error", "patients.csv not found.")
            log_event(self.username, self.role, "AddPatient (file missing)", "failed")
            return

        try:
            with open("Data/patients.csv", "a", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=self.fields)

                if os.path.getsize("Data/patients.csv") == 0:
                    writer.writeheader()

                writer.writerow(new_data)

            messagebox.showinfo("Success", "Patient added successfully!")
            log_event(self.username, self.role, f"AddPatient {new_data['patient_id']}", "success")

            for entry in self.entries.values():
                entry.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to add patient.\n{e}")
            log_event(self.username, self.role, "AddPatient (exception)", "failed")


# ============================================================
# REMOVE PATIENT
# ============================================================
class RemovePatientWindow:
    def __init__(self, root, username, role):
        self.root = tk.Toplevel(root)
        self.root.title("Remove Patient")
        self.username = username
        self.role = role

        tk.Label(self.root, text="Enter Patient ID to Remove:").grid(row=0, column=0, padx=10, pady=10)
        self.patient_id_entry = tk.Entry(self.root)
        self.patient_id_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Button(self.root, text="Remove", command=self.remove_patient).grid(row=1, column=0, columnspan=2, pady=10)

    def remove_patient(self):
        raw_id = self.patient_id_entry.get().strip()
        patient_id = normalize_id(raw_id)

        if not raw_id:
            messagebox.showerror("Error", "Please enter a Patient ID.")
            log_event(self.username, self.role, "RemovePatient (empty id)", "failed")
            return

        try:
            with open("Data/patients.csv", "r") as f:
                reader = list(csv.DictReader(f))

            updated_rows = [row for row in reader if normalize_id(row["patient_id"]) != patient_id]

            if len(updated_rows) == len(reader):
                messagebox.showerror("Error", "Patient ID not found.")
                log_event(self.username, self.role, f"RemovePatient {raw_id} (not found)", "failed")
                return

            with open("Data/patients.csv", "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=reader[0].keys())
                writer.writeheader()
                writer.writerows(updated_rows)

            messagebox.showinfo("Success", f"Patient {raw_id} removed successfully!")
            log_event(self.username, self.role, f"RemovePatient {raw_id}", "success")

        except FileNotFoundError:
            messagebox.showerror("Error", "patients.csv not found.")
            log_event(self.username, self.role, "RemovePatient (file missing)", "failed")


# ============================================================
# COUNT VISITS (CLINICIAN)
# ============================================================
class CountVisitsWindow:
    def __init__(self, root, username, role):
        self.root = tk.Toplevel(root)
        self.root.title("Count Visits")
        self.username = username
        self.role = role

        tk.Label(self.root, text="Enter Patient ID:").grid(row=0, column=0, padx=10, pady=10)
        self.patient_id_entry = tk.Entry(self.root)
        self.patient_id_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Button(self.root, text="Count", command=self.count_visits).grid(row=1, column=0, columnspan=2, pady=10)

    def count_visits(self):
        raw_id = self.patient_id_entry.get().strip()
        patient_id = normalize_id(raw_id)

        if not raw_id:
            messagebox.showerror("Error", "Please enter a Patient ID.")
            log_event(self.username, self.role, "CountVisits (empty id)", "failed")
            return

        try:
            with open("Data/encounters.csv", "r") as f:
                reader = csv.DictReader(f)
                count = sum(1 for row in reader if normalize_id(row["patient_id"]) == patient_id)

            messagebox.showinfo("Visit Count", f"Patient {raw_id} has {count} visits.")
            log_event(self.username, self.role, f"CountVisits {raw_id} -> {count}", "success")

        except FileNotFoundError:
            messagebox.showerror("Error", "encounters.csv not found.")
            log_event(self.username, self.role, "CountVisits (file missing)", "failed")


# ============================================================
# VIEW NOTE (OPTION B — FULL DETAILS)
# ============================================================
class ViewNoteWindow:
    def __init__(self, root, username, role):
        self.root = tk.Toplevel(root)
        self.root.title("View Notes")
        self.username = username
        self.role = role

        tk.Label(self.root, text="Enter Patient ID:").grid(row=0, column=0, padx=10, pady=10)
        self.patient_id_entry = tk.Entry(self.root)
        self.patient_id_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Button(self.root, text="View Notes", command=self.view_notes).grid(row=1, column=0, columnspan=2, pady=10)

    def view_notes(self):
        raw_id = self.patient_id_entry.get().strip()
        patient_id = normalize_id_3(raw_id)

        if not raw_id:
            messagebox.showerror("Error", "Please enter a Patient ID.")
            log_event(self.username, self.role, "ViewNotes (empty id)", "failed")
            return

        try:
            with open("Data/notes.csv", "r") as f:
                reader = csv.DictReader(f)
                notes = [row for row in reader if row["Patient_ID"] == patient_id]

            if not notes:
                messagebox.showinfo("No Notes", f"No notes found for patient {raw_id}.")
                log_event(self.username, self.role, f"ViewNotes {raw_id} (no notes)", "failed")
                return

            notes_window = tk.Toplevel(self.root)
            notes_window.title(f"Notes for {raw_id}")

            text_box = tk.Text(notes_window, wrap="word", width=70, height=25)
            text_box.pack(side="left", fill="both", expand=True)

            scrollbar = tk.Scrollbar(notes_window, command=text_box.yview)
            scrollbar.pack(side="right", fill="y")

            text_box.config(yscrollcommand=scrollbar.set)

            for n in notes:
                text_box.insert(tk.END, f"Note ID: {n['Note_ID']}\n")
                text_box.insert(tk.END, f"Date: {n['Date']}\n")
                text_box.insert(tk.END, f"Note:\n{n['Note_Text']}\n")
                text_box.insert(tk.END, "-" * 60 + "\n")

            log_event(self.username, self.role, f"ViewNotes {raw_id}", "success")

        except FileNotFoundError:
            messagebox.showerror("Error", "notes.csv not found.")
            log_event(self.username, self.role, "ViewNotes (file missing)", "failed")


# ============================================================
# ADMIN: COUNT ENCOUNTERS PER PATIENT
# ============================================================
class CountEncountersPerPatientWindow:
    def __init__(self, root, username, role):
        self.root = tk.Toplevel(root)
        self.root.title("Count Encounters Per Patient")
        self.username = username
        self.role = role

        tk.Label(self.root, text="Enter Patient ID:").grid(row=0, column=0, padx=10, pady=10)
        self.patient_id_entry = tk.Entry(self.root)
        self.patient_id_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Button(self.root, text="Count", command=self.count_encounters).grid(row=1, column=0, columnspan=2, pady=10)

    def count_encounters(self):
        raw_id = self.patient_id_entry.get().strip()
        patient_id = normalize_id(raw_id)

        if not raw_id:
            messagebox.showerror("Error", "Please enter a Patient ID.")
            log_event(self.username, self.role, "CountEncountersPerPatient (empty id)", "failed")
            return

        try:
            with open("Data/encounters.csv", "r") as f:
                reader = csv.DictReader(f)
                count = sum(1 for row in reader if normalize_id(row["patient_id"]) == patient_id)

            messagebox.showinfo("Encounters Per Patient", f"Patient {raw_id} has {count} encounters.")
            log_event(self.username, self.role, f"CountEncountersPerPatient {raw_id} -> {count}", "success")

        except FileNotFoundError:
            messagebox.showerror("Error", "encounters.csv not found.")
            log_event(self.username, self.role, "CountEncountersPerPatient (file missing)", "failed")


# ============================================================
# ADMIN: COUNT ENCOUNTERS BY DEPARTMENT
# ============================================================
class CountEncountersByDepartmentWindow:
    def __init__(self, root, username, role):
        self.root = tk.Toplevel(root)
        self.root.title("Count Encounters by Department")
        self.username = username
        self.role = role

        tk.Label(self.root, text="Enter Department ID (e.g., D1):").grid(row=0, column=0, padx=10, pady=10)
        self.dept_entry = tk.Entry(self.root)
        self.dept_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Button(self.root, text="Count", command=self.count_encounters).grid(row=1, column=0, columnspan=2, pady=10)

    def count_encounters(self):
        dept_id = self.dept_entry.get().strip().upper()

        if not dept_id:
            messagebox.showerror("Error", "Please enter a Department ID.")
            log_event(self.username, self.role, "CountEncountersByDepartment (empty id)", "failed")
            return

        try:
            with open("Data/encounters.csv", "r") as f:
                reader = csv.DictReader(f)
                count = sum(1 for row in reader if row["department_id"].upper() == dept_id)

            messagebox.showinfo("Encounters by Department", f"Department {dept_id} has {count} encounters.")
            log_event(self.username, self.role, f"CountEncountersByDepartment {dept_id} -> {count}", "success")

        except FileNotFoundError:
            messagebox.showerror("Error", "encounters.csv not found.")
            log_event(self.username, self.role, "CountEncountersByDepartment (file missing)", "failed")


# ============================================================
# MANAGEMENT: MONITOR PROVIDER WORKLOAD
# ============================================================
class MonitorProviderWorkloadWindow:
    def __init__(self, root, username, role):
        self.root = tk.Toplevel(root)
        self.root.title("Monitor Provider Workload")
        self.username = username
        self.role = role

        tk.Label(self.root, text="Enter Provider ID (e.g., PR1):").grid(row=0, column=0, padx=10, pady=10)
        self.provider_entry = tk.Entry(self.root)
        self.provider_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Button(self.root, text="Check Workload", command=self.check_workload).grid(row=1, column=0, columnspan=2, pady=10)

    def check_workload(self):
        provider_id = self.provider_entry.get().strip().upper()

        if not provider_id:
            messagebox.showerror("Error", "Please enter a Provider ID.")
            log_event(self.username, self.role, "MonitorProviderWorkload (empty id)", "failed")
            return

        try:
            with open("Data/encounters.csv", "r") as f:
                reader = csv.DictReader(f)
                count = sum(1 for row in reader if row["provider_id"].upper() == provider_id)

            messagebox.showinfo("Provider Workload", f"Provider {provider_id} has {count} encounters.")
            log_event(self.username, self.role, f"MonitorProviderWorkload {provider_id} -> {count}", "success")

        except FileNotFoundError:
            messagebox.showerror("Error", "encounters.csv not found.")
            log_event(self.username, self.role, "MonitorProviderWorkload (file missing)", "failed")
