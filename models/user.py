import uuid
from datetime import datetime

class User:
    _users = {}

    def __init__(self, email, first_name, last_name):
        if email in User._users:
            raise ValueError("A user with this email already exists.")
        self.id = str(uuid.uuid4())
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        self.updated_at = datetime.now()
        User._users[self.email] = self
        # Add logic to save the user to persistence layer

    def __repr__(self):
        return f'<User {self.email}>'