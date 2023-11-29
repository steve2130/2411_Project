from src.db import get_connection


class UserModel:
    """
    A class to interact with the users table in the database.
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

    def find(self, id_: int):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = :id", {'id': id_})
        return cursor.fetchone()

    def find_by_username(self, username: str):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = :username", {'username': username})
        return cursor.fetchone()

    def update(self, id_: int, avatar_url: str = None, password: str = None, is_admin: bool = None):
        cursor = self.connection.cursor()

        fields = []
        if avatar_url is not None:
            fields.append('avatar_url = :avatar_url')
        if password is not None:
            fields.append('password = :password')
        if is_admin is not None:
            fields.append('is_admin = :is_admin')

        cursor.execute("""
            UPDATE users
            SET """ + ', '.join(fields) + """
            WHERE id = :id
            """, {'id': id_, 'avatar_url': avatar_url, 'password': password, 'is_admin': is_admin})
        self.connection.commit()

    def delete(self, id_: int):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM users WHERE id = :id", {'id': id_})
        self.connection.commit()
