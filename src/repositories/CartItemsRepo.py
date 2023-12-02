from models.CartItems import CartItemsModel

# Table Name = CART_ITEMS

class CartItemsRepository:

    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor


    def Commit(self):
        """
        Upload the changes to database
        """
        self.connection.commit()


    def AddRecord(self, ID: int, USER_ID: int, PRODUCT_SKU_ID: int, AMOUNT: int):
        """
        Add one record to table

        Accept: (dict) {"ID": ?, "USER_ID": ?, "PRODUCT_SKU_ID": ?, "AMOUNT": ?}
        """
        # Accept dict only 
        self.cursor.execute("""
                            INSERT INTO CART_ITEMS (ID, USER_ID, PRODUCT_SKU_ID, AMOUNT)
                            VALUES (:ID, :USER_ID, :PRODUCT_SKU_ID, :AMOUNT)
                            """, ID=ID, USER_ID=USER_ID, PRODUCT_SKU_ID=PRODUCT_SKU_ID, AMOUNT=AMOUNT)
        
        

    def GetRecord(self, column, query):
        """
        Get one/many record(s) based on the query given (e.g. ID = 10)

        Input:
            column (str) -> A column of the table (e.g. ID, NAME)
            query (str)  -> Searching condition IN SQL FORMAT!!!!!! (e.g. ID = 10)

        Output:
            List of filtered search result
        """
        statement = f"SELECT {str(column)} FROM CART_ITEMS WHERE {str(query)}"

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

        statement = f"""DELETE FROM CART_ITEMS
                        WHERE {str(column)} = {str(query)}
                     """
        self.cursor.execute(statement)



    def UpdateRecord(self, ID: int, USER_ID: int, PRODUCT_SKU_ID: int, AMOUNT: int) -> None:
        """
        Update a record (searched with ID) with the changed attribute
        
        Input: ID: int, USER_ID: int, PRODUCT_SKU_ID: int, AMOUNT: int
        """
        self.cursor.execute("""
                            UPDATE CART_ITEMS
                            SET :USER_ID, :PRODUCT_SKU_ID, :AMOUNT
                            WHERE :ID, 
                            """, USER_ID=USER_ID, PRODUCT_SKU_ID=PRODUCT_SKU_ID, AMOUNT=AMOUNT, ID=ID)


    def ReturnNumberOfEntries(self):
        NumberOfEntries = self.cursor.execute("SELECT COUNT(*) FROM CART_ITEMS")
        return NumberOfEntries