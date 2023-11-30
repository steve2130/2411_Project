from src.db import get_connection
from src.models import Products

class ProductRepository:

    def __init__(self):
        self.connection = get_connection()
        self.cursor = self.connection.cursor()

    def AddRecord(self, entity=Products):
        """
        Add one record to Prodcuts
        Accept: (dict) "ID": ?, "CATEGORY_ID": ?, "TITLE": ?, "DESCRIPTION": ?, "IMAGE_URL": ?, "PRICE": ?}
        """
        # Accept dict only 
        self.cursor.execute("""
                            INSERT INTO Products (ID, CATEGORY_ID, TITLE, DESCRIPTION, IMAGE_URL, PRICE)
                            VALUES (:ID, :CATEGORY_ID, :TITLE, :DESCRIPTION, :IMAGE_URL, :PRICE)
                            """, entity.to_db)
        
    def GetRecord(self, query):
        self.cursor.execute("""""")

    def Commit(self):
        self.connection.commit()