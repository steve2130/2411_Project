#from db import get_connection
from models.Products import ProductModel

class ProductRepository:

    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor


    def Commit(self):
        """
        Upload the changes to database
        """
        self.connection.commit()


    def AddRecord(self, ID: int, CATEGORY_ID: int, TITLE: str, DESCRIPTION: str, IMAGE_URL: str, PRICE: float):
        """
        Add one record to Prodcuts

        Accept: (dict) {"ID": ?, "CATEGORY_ID": ?, "TITLE": ?, "DESCRIPTION": ?, "IMAGE_URL": ?, "PRICE": ?}
        """
        # Accept dict only 
        self.cursor.execute("""
                            INSERT INTO Products (ID, CATEGORY_ID, TITLE, DESCRIPTION, IMAGE_URL, PRICE)
                            VALUES (:ID, :CATEGORY_ID, :TITLE, :DESCRIPTION, :IMAGE_URL, :PRICE)
                            """, ID=ID, CATEGORY_ID=CATEGORY_ID, TITLE=TITLE, DESCRIPTION=DESCRIPTION, IMAGE_URL=IMAGE_URL, PRICE=PRICE)
        

    def GetRecord(self, column: str, query: str):
        """
        Get one/many record(s) based on the query given (e.g. PRICE > 10)

        Input:
            column (str) -> A column of the table (e.g. ID, CATEGORY_ID, TITLE, ...)
            query (str)  -> Searching condition IN SQL FORMAT!!!!!! (e.g. PRICE > 10)

        Output:
            List of filtered search result
        """

        # For some unknown reason, you can't use bind variables like this:

        # self.cursor.execute("""
        #                     SELECT :column FROM PRODUCTS WHERE :query
        #                     """, column=column, query=query)


        search = f"SELECT {str(column)} FROM PRODUCTS WHERE {str(query)}"

        self.cursor.execute(search)
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


    def UpdateRecord(self,  ID: int, CATEGORY_ID: int, TITLE: str, DESCRIPTION: str, IMAGE_URL: str, PRICE: float) -> None:
        """
        Update a record (searched with ID) with the changed attribute (change with setter in Product.py)
        ID: int, CATEGORY_ID: int, TITLE: str, DESCRIPTION: str, IMAGE_URL: str, PRICE: float,
        """
        self.cursor.execute("""
                            UPDATE PRODUCTS
                            SET :CATEGORY_ID, :TITLE, :DESCRIPTION, :IMAGE_URL, :PRICE
                            WHERE :ID
                            """, CATEGORY_ID=CATEGORY_ID, TITLE=TITLE, DESCRIPTION=DESCRIPTION, IMAGE_URL=IMAGE_URL, PRICE=PRICE, ID=ID)
