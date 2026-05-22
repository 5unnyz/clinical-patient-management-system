import sys, os
sys.path.append(os.path.abspath("src"))

from src.data_manager import DataManager
from src.user import UserManager


class UIApp:
    """
    Text-based UI for the Final Project.
    Handles login, menus, analytics, and output saving.
    """

    def __init__(self):
        self.user_manager = UserManager()
        self.data_manager = DataManager()
        self.logged_in_user = None

    # -------------------------
    # LOGIN SCREEN
    # -------------------------
    def login(self):
        print("\n=== LOGIN ===")
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        if self.user_manager.authenticate(username, password):
            self.logged_in_user = self.user_manager.get_user(username)
            print(f"\nWelcome, {username}!")
            return True
        else:
            print("\nInvalid username or password.")
            return False

    # -------------------------
    # MAIN MENU
    # -------------------------
    def main_menu(self):
        while True:
            print("\n=== MAIN MENU ===")
            print("1. Load Data")
            print("2. View Analytics")
            print("3. Save Report")
            print("4. View Usage Log")
            print("5. Exit")

            choice = input("Choose an option: ").strip()

            if choice == "1":
                self.load_data_screen()
            elif choice == "2":
                self.analytics_menu()
            elif choice == "3":
                self.save_report_screen()
            elif choice == "4":
                self.view_usage_log()
            elif choice == "5":
                print("\nGoodbye!")
                break
            else:
                print("Invalid choice. Try again.")

    # -------------------------
    # LOAD DATA
    # -------------------------
    def load_data_screen(self):
        print("\nLoading data...")
        self.data_manager.load_all_data()
        print("Data loaded and linked successfully!")

    # -------------------------
    # ANALYTICS MENU
    # -------------------------
    def analytics_menu(self):
        while True:
            print("\n=== ANALYTICS MENU ===")
            print("1. Average BMI")
            print("2. Average A1C")
            print("3. Smoking Rate")
            print("4. Gender Counts")
            print("5. High A1C Patients")
            print("6. Encounters by Department")
            print("7. Total Procedure Cost")
            print("8. Back to Main Menu")

            choice = input("Choose an option: ").strip()

            if choice == "1":
                print("\nAverage BMI:", self.data_manager.get_average_bmi())

            elif choice == "2":
                print("\nAverage A1C:", self.data_manager.get_average_a1c())

            elif choice == "3":
                print("\nSmoking Rate:", self.data_manager.get_smoking_rate())

            elif choice == "4":
                print("\nGender Counts:", self.data_manager.get_gender_counts())

            elif choice == "5":
                threshold = float(input("Enter A1C threshold: "))
                results = self.data_manager.get_high_a1c_patients(threshold)
                print(f"\nPatients with A1C >= {threshold}: {len(results)}")

            elif choice == "6":
                print("\nEncounters by Department:", self.data_manager.get_encounters_by_department())

            elif choice == "7":
                print("\nTotal Procedure Cost:", self.data_manager.get_total_procedure_cost())

            elif choice == "8":
                break

            else:
                print("Invalid choice. Try again.")

    # -------------------------
    # SAVE REPORT
    # -------------------------
    def save_report_screen(self):
        print("\n=== SAVE REPORT ===")
        filename = input("Enter filename (e.g., report.txt): ").strip()

        content = "=== SYSTEM REPORT ===\n"
        content += f"Average BMI: {self.data_manager.get_average_bmi()}\n"
        content += f"Average A1C: {self.data_manager.get_average_a1c()}\n"
        content += f"Smoking Rate: {self.data_manager.get_smoking_rate()}\n"
        content += f"Gender Counts: {self.data_manager.get_gender_counts()}\n"
        content += f"Total Procedure Cost: {self.data_manager.get_total_procedure_cost()}\n"

        path = self.data_manager.save_output(filename, content)
        print(f"\nReport saved to: {path}")

    # -------------------------
    # VIEW USAGE LOG
    # -------------------------
    def view_usage_log(self):
        print("\n=== USAGE LOG ===")
        for action in self.data_manager.get_usage_log():
            print("-", action)
