from models import User


class UserRepository:
    """
    A class to interact with the users table in the database.
    """


    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor


    def create(self, username: str, avatar_url: str, password: str, is_admin: bool):
        self.cursor.execute("""
            INSERT INTO users (username, avatar_url, password, is_admin)
            VALUES (:username, :avatar_url, :password, :is_admin)
        """, username=username, avatar_url=avatar_url, password=password, is_admin=is_admin)
        self.connection.commit()

    def find(self, id_: int) -> User or None:
        self.cursor.execute("SELECT * FROM users WHERE id = :id", {'id': id_})
        return self.cursor.fetchone()

    def find_by_username(self, username: str) -> User or None:
        self.cursor.execute("SELECT * FROM users WHERE username = :username", {'username': username})
        return self.cursor.fetchone()

    def update(self, id_: int, data: dict):
        fields = []
        if 'avatar_url' in data:
            fields.append('avatar_url = :avatar_url')
        if 'password' in data:
            fields.append('password = :password')
        if 'is_admin' in data:
            fields.append('is_admin = :is_admin')

        data['id'] = id_
        self.cursor.execute("""
                            UPDATE users
                            SET """ + ', '.join(fields) + """
                            WHERE id = :id
                            """, data)
        self.connection.commit()

    def delete(self, id_: int):
        self.cursor.execute("DELETE FROM users WHERE id = :id", {'id': id_})
        self.connection.commit()


    def ReturnNumberOfEntries(self):
        NumberOfEntries = self.cursor.execute("SELECT COUNT(*) FROM users")
        return NumberOfEntries