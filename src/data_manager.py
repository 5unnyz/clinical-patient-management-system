import os
import sys

# Ensure src/ is in the path
sys.path.append(os.path.abspath("src"))

from pa2.utils.data_loaders import (
    load_patients,
    load_providers,
    load_departments,
    load_encounters,
    load_procedures
)
from pa2.utils.linker import link_data
from pa2.utils import analytics


class DataManager:
    """
    Central controller for all data operations.
    Loads PA2 data, links it, and exposes analytics functions.
    """

    def __init__(self, data_folder="Data", output_folder="output"):
        self.data_folder = data_folder
        self.output_folder = output_folder

        # Data containers
        self.patients = {}
        self.providers = {}
        self.departments = {}
        self.encounters = {}
        self.procedures = {}

        # Usage tracking
        self.usage_log = []

    # -------------------------
    # DATA LOADING
    # -------------------------
    def load_all_data(self):
        """Loads all PA2 CSV files and links them."""
        self.patients = load_patients(os.path.join(self.data_folder, "patients.csv"))
        self.providers = load_providers(os.path.join(self.data_folder, "providers.csv"))
        self.departments = load_departments(os.path.join(self.data_folder, "departments.csv"))
        self.encounters = load_encounters(os.path.join(self.data_folder, "encounters.csv"))
        self.procedures = load_procedures(os.path.join(self.data_folder, "procedures.csv"))

        # Link everything
        link_data(
            self.patients,
            self.providers,
            self.departments,
            self.encounters,
            self.procedures
        )

        return True

    # -------------------------
    # ANALYTICS WRAPPERS
    # -------------------------
    def get_average_bmi(self):
        self._log("Average BMI")
        return analytics.average_bmi(self.patients)

    def get_average_a1c(self):
        self._log("Average A1C")
        return analytics.average_a1c(self.patients)

    def get_smoking_rate(self):
        self._log("Smoking Rate")
        return analytics.smoking_rate(self.patients)

    def get_gender_counts(self):
        self._log("Gender Counts")
        return analytics.count_patients_by_gender(self.patients)

    def get_high_a1c_patients(self, threshold=6.5):
        self._log(f"High A1C >= {threshold}")
        return analytics.get_high_a1c_patients(self.patients, threshold)

    def get_encounters_by_department(self):
        self._log("Encounters by Department")
        return analytics.encounters_per_department(self.encounters)

    def get_total_procedure_cost(self):
        self._log("Total Procedure Cost")
        return analytics.total_procedure_cost(self.procedures)

    # -------------------------
    # OUTPUT SAVING
    # -------------------------
    def save_output(self, filename, content):
        """Saves text output to the output folder."""
        os.makedirs(self.output_folder, exist_ok=True)
        path = os.path.join(self.output_folder, filename)

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        self._log(f"Saved output: {filename}")
        return path

    # -------------------------
    # USAGE LOGGING
    # -------------------------
    def _log(self, action):
        self.usage_log.append(action)

    def get_usage_log(self):
        return self.usage_log
