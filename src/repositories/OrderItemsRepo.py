from db import get_connection
from models.OrderItems import OrderItemsModel

# Table Name = ORDER_ITEMS

class OrderItemsRepository:

    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor


    def Commit(self):
        """
        Upload the changes to database
        """
        self.connection.commit()


    def AddRecord(self, ID: int, ORDER_ID: int, PRODUCT_ID: int, PRODUCT_SKU_ID: int, AMOUNT: int, PRICE: float):
        """
        Add one record to table

        Accept: (dict) {"ID": ?, "ORDER_ID": ?, "PRODUCT_ID": ?, "PRODUCT_SKU_ID": ?, "AMOUNT": ?, "PRICE": ?}
        """
        # Accept dict only 
        self.cursor.execute("""
                            INSERT INTO ORDER_ITEMS (ID, ORDER_ID, PRODUCT_ID, PRODUCT_SKU_ID, AMOUNT, PRICE)
                            VALUES (:ID, :ORDER_ID, :PRODUCT_ID, :PRODUCT_SKU_ID, :AMOUNT, :PRICE)
                            """, ID=ID, ORDER_ID=ORDER_ID, PRODUCT_ID=PRODUCT_ID, PRODUCT_SKU_ID=PRODUCT_SKU_ID, AMOUNT=AMOUNT, PRICE=PRICE)
        
        

    def GetRecord(self, column, query):
        """
        Get one/many record(s) based on the query given (e.g. ID = 10)

        Input:
            column (str) -> A column of the table (e.g. ID, NAME)
            query (str)  -> Searching condition IN SQL FORMAT!!!!!! (e.g. ID = 10)

        Output:
            List of filtered search result
        """
        statement = f"SELECT {str(column)} FROM ORDER_ITEMS WHERE {str(query)}"

        self.cursor.execute(statement)
        results =  self.cursor.fetchall()
        return [result for result in results]



    def DeleteRecord(self, column, query):
        """
        Delete one record from the table

        Input:
            column (str) & query (str) -> To find the specificed record (e.g. WHERE ID = 10)
                                                                               (column)  (query)
        """

        statement = f"""DELETE FROM ORDER_ITEMS
                        WHERE {str(column)} = {str(query)}
                     """
        self.cursor.execute(statement)



    def UpdateRecord(self, ID: int, ORDER_ID: int, PRODUCT_ID: int, PRODUCT_SKU_ID: int, AMOUNT: int, PRICE: float) -> None:
        """
        Update a record (searched with ID) with the changed attribute
        """
        self.cursor.execute("""
                            UPDATE ORDER_ITEMS
                            SET :ORDER_ID, :PRODUCT_ID, :PRODUCT_SKU_ID, :AMOUNT, :PRICE
                            WHERE :ID, 
                            """, ORDER_ID=ORDER_ID, PRODUCT_ID=PRODUCT_ID, PRODUCT_SKU_ID=PRODUCT_SKU_ID, AMOUNT=AMOUNT, PRICE=PRICE, ID=ID)
