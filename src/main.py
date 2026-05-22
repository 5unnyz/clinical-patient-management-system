import tkinter as tk
from src.gui_login import LoginWindow
from src.gui_menu import MenuWindow
from src.logger import log_event

def start_app(username, role):
    # log successful login
    log_event(username, role, "login", "success")

    root = tk.Tk()
    MenuWindow(root, username, role)
    root.mainloop()

def main():
    root = tk.Tk()
    LoginWindow(root, start_app)
    root.mainloop()

if __name__ == "__main__":
    main()
