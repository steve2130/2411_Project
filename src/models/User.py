from src.db import get_connection


class UserModel:
    """
    A class to interact with the users table in the database.

    :class:`UserService` is recommended to use over this class.
    """

    def __init__(self):
        self.connection = get_connection()

    def create(self, username: str, avatar_url: str, password: str, is_admin: bool):
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO users (username, avatar_url, password, is_admin)
            VALUES (:username, :avatar_url, :password, :is_admin)
        """, {'username': username, 'avatar_url': avatar_url, 'password': password, 'is_admin': is_admin})
        self.connection.commit()

    def get(self, id_: int):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = :id", {'id': id_})
        return cursor.fetchone()

    def get_by_username(self, username: str):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = :username", {'username': username})
        return cursor.fetchone()

    def update(self, id_: int, username: str, avatar_url: str, password: str, is_admin: bool):
        cursor = self.connection.cursor()
        cursor.execute("""
            UPDATE users
            SET username = :username, avatar_url = :avatar_url, password = :password, is_admin = :is_admin
            WHERE id = :id
        """, {'id': id_, 'username': username, 'avatar_url': avatar_url, 'password': password, 'is_admin': is_admin})
        self.connection.commit()

    def delete(self, id_: int):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM users WHERE id = :id", {'id': id_})
        self.connection.commit()
