from Model.user import User
from Persistence.persistence_manager import IPersistenceManager


class UserRepo(IPersistenceManager):
    """Clase para gestionar la persistencia de usuarios."""

    def __init__(self):
        """Inicializa UserRepo con un diccionario vacío
        y un contador next_id."""
        self.users = {}
        self.next_id = 1

    def save(self, user):
        """
        Guarda un usuario.
        """
        if not hasattr(user, 'user_id'):
            user.user_id = self.next_id
            self.next_id += 1
        self.users[user.user_id] = user

    def get(self, user_id):
        """
        Obtiene un usuario por su ID.
        """
        return self.users.get(user_id)

    def get_all(self):
        """
        Obtiene todos los usuarios.
        """
        return list(self.users.values())

    def update(self, user_id, new_user_data):
        """
        Actualiza un usuario existente.
        """
        if user_id in self.users:
            user = self.users[user_id]
            user.update_user_data(new_user_data)
            self.save(user)
            return True
        return False

    def delete(self, user_id):
        """
        Elimina un usuario existente.
        """
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False
