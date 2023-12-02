class AddressRepository:
    """
    A class to interact with the addresses table in the database.
    """

    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor


    def create(self, user_id: int, contact_name: str, contact_phone: str, details: str):
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO addresses (user_id, contact_name, contact_phone, details)
            VALUES (:user_id, :contact_name, :contact_phone, :details)
        """, user_id=user_id, contact_name=contact_name, contact_phone=contact_phone, details=details)
        self.connection.commit()

    def find(self, id_: int):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM addresses WHERE id = :id", {'id': id_})
        return cursor.fetchone()

    def get_by_user_id(self, user_id: int):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM addresses WHERE user_id = :user_id", user_id=user_id)
        return cursor.fetchall()

    def update(self, id_: int, contact_name: str, contact_phone: str, details: str):
        cursor = self.connection.cursor()
        cursor.execute("""
            UPDATE addresses
            SET contact_name = :contact_name, contact_phone = :contact_phone, details = :details
            WHERE id = :id
        """, id=id_, contact_name=contact_name, contact_phone=contact_phone, details=details)
        self.connection.commit()

    def delete(self, id_: int):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM addresses WHERE id = :id", {'id': id_})
        self.connection.commit()


    def ReturnNumberOfEntries(self):
        NumberOfEntries = self.cursor.execute("SELECT COUNT(*) FROM addresses")
        NumberOfEntries = self.cursor.fetchone()
        return int(NumberOfEntries)