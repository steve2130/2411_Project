from src.db import get_connection
from src.models import User


class UserRepository:
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
        """, username=username, avatar_url=avatar_url, password=password, is_admin=is_admin)
        self.connection.commit()

    def find(self, id_: int) -> User or None:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = :id", {'id': id_})
        return cursor.fetchone()

    def find_by_username(self, username: str) -> User or None:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = :username", {'username': username})
        return cursor.fetchone()

    def update(self, id_: int, data: dict):
        cursor = self.connection.cursor()

        fields = []
        if 'avatar_url' in data:
            fields.append('avatar_url = :avatar_url')
        if 'password' in data:
            fields.append('password = :password')
        if 'is_admin' in data:
            fields.append('is_admin = :is_admin')

        data['id'] = id_
        cursor.execute("""
            UPDATE users
            SET """ + ', '.join(fields) + """
            WHERE id = :id
            """, data)
        self.connection.commit()

    def delete(self, id_: int):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM users WHERE id = :id", {'id': id_})
        self.connection.commit()
