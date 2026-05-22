class User:
    """
    Represents a system user with username + password.
    Handles login validation and tracking login attempts.
    """

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.login_attempts = 0

    def check_password(self, entered_password: str) -> bool:
        """Returns True if password matches."""
        self.login_attempts += 1
        return self.password == entered_password


class UserManager:
    """
    Stores multiple users and handles login authentication.
    """

    def __init__(self):
        # Hardcoded users for Final Project
        self.users = {
            "admin": User("admin", "admin123"),
            "sunny": User("sunny", "password"),
            "guest": User("guest", "guest")
        }

    def authenticate(self, username: str, password: str) -> bool:
        """Validates username + password."""
        if username not in self.users:
            return False

        user = self.users[username]
        return user.check_password(password)

    def get_user(self, username: str):
        """Returns the User object if exists."""
        return self.users.get(username)
