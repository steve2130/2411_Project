from models.Orders import OrdersModel

# Table Name = ORDERS

class OrdersRepository:

    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor


    def Commit(self):
        """
        Upload the changes to database
        """
        self.connection.commit()


    def AddRecord(self, ID: int, USER_ID: int, ADDRESS_ID: int, TOTAL_AMOUNT: int, REMARK: str, PAID_AT:str, PAYMENT_METHOD: str, PAYMENT_NO: str, SHIPMENT_STATUS: str, SHIPMENT_DATA: str, REFUND_STATUS: str, REFUND_NO: str, CLOSED:str):
        """
        Add one record to table

        Accept: (dict) {"ID": ?, "USER_ID": ?, "ADDRESS_ID": ?, "TOTAL_AMOUNT": ?, "REMARK": ?, "PAID_AT": ?, "PAYMENT_METHOD": ?, "PAYMENT_NO": ?, "SHIPMENT_STATUS": ?, "SHIPMENT_DATA": ?, "REFUND_STATUS": ?, "REFUND_NO": ?, "CLOSED": char}
        """
        # Accept dict only 
        self.cursor.execute("""
                            INSERT INTO ORDERS (ID, USER_ID, ADDRESS_ID, TOTAL_AMOUNT, REMARK, PAID_AT, PAYMENT_METHOD, PAYMENT_NO, SHIPMENT_STATUS, SHIPMENT_DATA, REFUND_STATUS, REFUND_NO, CLOSED)
                            VALUES (:ID, :USER_ID, :ADDRESS_ID, :TOTAL_AMOUNT, :REMARK, :PAID_AT, :PAYMENT_METHOD, :PAYMENT_NO, :SHIPMENT_STATUS, :SHIPMENT_DATA, :REFUND_STATUS, :REFUND_NO, :CLOSED)
                            """, ID=ID, USER_ID=USER_ID, ADDRESS_ID=ADDRESS_ID, TOTAL_AMOUNT=TOTAL_AMOUNT, REMARK=REMARK, PAID_AT=PAID_AT, PAYMENT_METHOD=PAYMENT_METHOD, PAYMENT_NO=PAYMENT_NO, SHIPMENT_STATUS=SHIPMENT_STATUS, SHIPMENT_DATA=SHIPMENT_DATA, REFUND_STATUS=REFUND_STATUS, REFUND_NO=REFUND_NO, CLOSED=CLOSED)
        
        

    def GetRecord(self, column, query) -> OrdersModel or None:
        """
        Get one/many record(s) based on the query given (e.g. ID = 10)

        Input:
            column (str) -> A column of the table (e.g. ID, NAME)
            query (str)  -> Searching condition IN SQL FORMAT!!!!!! (e.g. ID = 10)

        Output:
            List of filtered search result
        """
        statement = f"SELECT {str(column)} FROM ORDERS {str(query)}"

        self.cursor.execute(statement)
        columns = [col[0] for col in self.cursor.description]
        self.cursor.rowfactory = lambda *args: dict(zip(columns, args))
        
        results =  self.cursor.fetchall()
        return results



    def DeleteRecord(self, column, query):
        """
        Delete one record from the table

        Input:
            column (str) & query (str) -> To find the specificed record (e.g. WHERE ID = 10)
                                                                               (column)  (query)
        """

        statement = f"""DELETE FROM ORDERS
                        WHERE {str(column)} = {str(query)}
                     """
        self.cursor.execute(statement)



    def UpdateRecord(self, ID: int, USER_ID: int, ADDRESS_ID: int, TOTAL_AMOUNT: int, REMARK: str, PAID_AT:str, PAYMENT_METHOD: str, PAYMENT_NO: str, SHIPMENT_STATUS: str, SHIPMENT_DATA: str, REFUND_STATUS: str, REFUND_NO: str, CLOSED:str) -> None:
        """
        Update a record (searched with ID) with the changed attribute
        
        Input: self, ID: int, USER_ID: int, ADDRESS_ID: int, TOTAL_AMOUNT: int, REMARK: str, PAID_AT:str, PAYMENT_METHOD: str, PAYMENT_NO: str, SHIPMENT_STATUS: str, SHIPMENT_DATA: str, REFUND_STATUS: str, REFUND_NO: str, CLOSED:str
        """
        self.cursor.execute("""
                            UPDATE ORDERS
                            SET :USER_ID, :ADDRESS_ID, :TOTAL_AMOUNT, :REMARK, :PAID_AT, :PAYMENT_METHOD, :PAYMENT_NO, :SHIPMENT_STATUS, :SHIPMENT_DATA, :REFUND_STATUS, :REFUND_NO, :CLOSED
                            WHERE :ID, 
                            """, USER_ID=USER_ID, ADDRESS_ID=ADDRESS_ID, TOTAL_AMOUNT=TOTAL_AMOUNT, REMARK=REMARK, PAID_AT=PAID_AT, PAYMENT_METHOD=PAYMENT_METHOD, PAYMENT_NO=PAYMENT_NO, SHIPMENT_STATUS=SHIPMENT_STATUS, SHIPMENT_DATA=SHIPMENT_DATA, REFUND_STATUS=REFUND_STATUS, REFUND_NO=REFUND_NO, CLOSED=CLOSED, ID=ID)




    def ReturnNumberOfEntries(self):
        NumberOfEntries = self.cursor.execute("SELECT COUNT(*) FROM ORDERS")
        return NumberOfEntries