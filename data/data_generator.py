import csv
import random
from datetime import datetime, timedelta

NUM_PATIENTS = 200
NUM_PROVIDERS = 20
NUM_ENCOUNTERS = 400
NUM_PROCEDURES = 250


def generate_patients():
    genders = ["Male", "Female"]

    rows = []

    for i in range(NUM_PATIENTS):

        patient = [
            f"P{i+1}",
            random.randint(18, 90),
            random.choice(genders),
            round(random.uniform(18, 40), 1),
            round(random.uniform(4.5, 10.0), 1),
            random.randint(100, 170),
            random.randint(60, 100),
            random.choice([True, False])
        ]

        rows.append(patient)

    with open("patients.csv", "w", newline="") as f:

        writer = csv.writer(f)

        writer.writerow([
            "patient_id", "age", "gender",
            "bmi", "a1c", "bp_sys", "bp_dia", "smoking"
        ])

        writer.writerows(rows)


def generate_providers():

    specialties = [
        "Cardiology",
        "Primary Care",
        "Endocrinology",
        "Pulmonology", 
        "Oncology",
        "Pediatric",
        "Emergency Medicine"
    ]

    rows = []

    for i in range(NUM_PROVIDERS):

        rows.append([
            f"PR{i+1}",
            f"Dr_{i+1}",
            random.choice(specialties),
            f"D{random.randint(1,4)}"
        ])

    with open("providers.csv", "w", newline="") as f:

        writer = csv.writer(f)

        writer.writerow([
            "provider_id",
            "name",
            "specialty",
            "department_id"
        ])

        writer.writerows(rows)


def generate_departments():

    departments = [
        ("D1", "Cardiology", "Building A"),
        ("D2", "Primary Care", "Building B"),
        ("D3", "Endocrinology", "Building C"),
        ("D4", "Pulmonology", "Building D")
    ]

    with open("departments.csv", "w", newline="") as f:

        writer = csv.writer(f)

        writer.writerow([
            "department_id",
            "name",
            "location"
        ])

        writer.writerows(departments)


def generate_encounters():

    encounter_types = ["Outpatient", "Inpatient", "Emergency"]

    rows = []

    for i in range(NUM_ENCOUNTERS):

        date = datetime.today() - timedelta(days=random.randint(0, 365))

        rows.append([
            f"E{i+1}",
            f"P{random.randint(1, NUM_PATIENTS)}",
            f"PR{random.randint(1, NUM_PROVIDERS)}",
            f"D{random.randint(1,4)}",
            date.strftime("%Y-%m-%d"),
            random.choice(encounter_types)
        ])

    with open("encounters.csv", "w", newline="") as f:

        writer = csv.writer(f)

        writer.writerow([
            "encounter_id",
            "patient_id",
            "provider_id",
            "department_id",
            "encounter_date",
            "encounter_type"
        ])

        writer.writerows(rows)


def generate_procedures():

    procedures = [
    ("93000", "Electrocardiogram"),
    ("80053", "Metabolic Panel"),
    ("83036", "Hemoglobin A1C Test"),
    ("71020", "Chest X-Ray"),

    ("85025", "Complete Blood Count"),
    ("80048", "Basic Metabolic Panel"),
    ("84443", "Thyroid Stimulating Hormone Test"),
    ("80061", "Lipid Panel"),
    ("85610", "Prothrombin Time Test"),

    ("81001", "Urinalysis"),
    ("82565", "Creatinine Blood Test"),
    ("82947", "Glucose Blood Test"),
    ("83540", "Iron Test"),
    ("84153", "Prostate Specific Antigen Test"),

    ("90658", "Influenza Vaccination"),
    ("90471", "Immunization Administration"),
    ("90715", "Tdap Vaccination"),
    ("90732", "Pneumococcal Vaccination"),

    ("71045", "Chest X-Ray Single View"),
    ("71250", "CT Scan Chest"),
    ("70450", "CT Scan Head"),
    ("74176", "CT Scan Abdomen"),

    ("93306", "Echocardiogram"),
    ("93880", "Carotid Ultrasound"),
    ("76700", "Abdominal Ultrasound"),

    ("45378", "Colonoscopy"),
    ("43235", "Upper GI Endoscopy"),
    ("99213", "Office Visit Established Patient"),

    ("12001", "Simple Wound Repair"),
    ("17000", "Skin Lesion Removal"),
    ("20610", "Joint Injection")]

    rows = []

    for i in range(NUM_PROCEDURES):

        code, name = random.choice(procedures)

        rows.append([
            f"PROC{i+1}",
            f"E{random.randint(1, NUM_ENCOUNTERS)}",
            f"P{random.randint(1, NUM_PATIENTS)}",
            code,
            name,
            round(random.uniform(100, 2000), 2)
        ])

    with open("procedures.csv", "w", newline="") as f:

        writer = csv.writer(f)

        writer.writerow([
            "procedure_id",
            "encounter_id",
            "patient_id",
            "procedure_code",
            "procedure_name",
            "cost"
        ])

        writer.writerows(rows)


def main():

    generate_patients()
    generate_providers()
    generate_departments()
    generate_encounters()
    generate_procedures()

    print("Synthetic dataset generated.")


if __name__ == "__main__":
    main()