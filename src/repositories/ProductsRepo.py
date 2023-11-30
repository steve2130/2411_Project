from src.db import get_connection
from src.models import Products

class ProductRepository:

    def __init__(self):
        self.connection = get_connection()
        self.cursor = self.connection.cursor()


    def Commit(self):
        """
        Upload the changes to database
        """
        self.connection.commit()


    def AddRecord(self, entity=Products):
        """
        Add one record to Prodcuts

        Accept: (dict) {"ID": ?, "CATEGORY_ID": ?, "TITLE": ?, "DESCRIPTION": ?, "IMAGE_URL": ?, "PRICE": ?}
        """
        # Accept dict only 
        self.cursor.execute("""
                            INSERT INTO Products (ID, CATEGORY_ID, TITLE, DESCRIPTION, IMAGE_URL, PRICE)
                            VALUES (:ID, :CATEGORY_ID, :TITLE, :DESCRIPTION, :IMAGE_URL, :PRICE)
                            """, entity.to_db)
        

    def GetRecord(self, column, query):
        """
        Get one/many record(s) based on the query given (e.g. PRICE > 10)

        Input:
            column (str) -> A column of the table (e.g. ID, CATEGORY_ID, TITLE, ...)
            query (str)  -> Searching condition IN SQL FORMAT!!!!!! (e.g. PRICE > 10)

        Output:
            List of filtered search result
        """
        self.cursor.execute("""
                            SELECT :column FROM PRODUCTS
                            WHERE :query
                            """, column=column, query=query)
        results =  self.cursor.fetchall()
        return [result for result in results]


    def DeleteRecord(self, column, query):
        """
        Delete one record from Products

        Input:
            column (str) & query (str) -> To find the specificed record (e.g. WHERE ID = 10)
                                                                               (column)  (query)
        """

        self.cursor.execute("""
                            DELETE FROM PRODUCTS
                            WHERE :column = :query
                            """, column=column, query=query)


    def UpdateRecord(self, entity: Products) -> None:
        """
        Update a record (searched with ID) with the changed attribute (change with setter in Product.py)
        """
        self.cursor.execute("""
                            UPDATE PRODUCTS
                            SET :CATEGORY_ID, :TITLE, :DESCRIPTION, :IMAGE_URL, :PRICE
                            WHERE :ID
                            """, CATEGORY_ID=entity.CATEGORY_ID, TITLE=entity.TITLE, DESCRIPTION=entity.DESCRIPTION, IMAGE_URL=entity.IMAGE_URL, PRICE=entity.PRICE, ID=entity.ID)
