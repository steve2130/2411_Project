from src.db import get_connection


class AddressRepository:
    """
    A class to interact with the addresses table in the database.
    """

    def __init__(self):
        self.connection = get_connection()

    def create(self, user_id: int, details: str):
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO addresses (user_id, details)
            VALUES (:user_id, :details)
        """, {'user_id': user_id, 'details': details})
        self.connection.commit()

    def find(self, id_: int):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM addresses WHERE id = :id", {'id': id_})
        return cursor.fetchone()

    def get_by_user_id(self, user_id: int):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM addresses WHERE user_id = :user_id", {'user_id': user_id})
        return cursor.fetchall()

    def update(self, id_: int, details: str):
        cursor = self.connection.cursor()
        cursor.execute("""
            UPDATE addresses
            SET details = :details
            WHERE id = :id
        """, {'id': id_, 'details': details})
        self.connection.commit()

    def delete(self, id_: int):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM addresses WHERE id = :id", {'id': id_})
        self.connection.commit()