from models.ProductSKUs import ProductSKUsModel

# Table name = PRODUCT_SKUS

class ProductSKUsRepository:

    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor


    def Commit(self):
        """
        Upload the changes to database
        """
        self.connection.commit()


    def AddRecord(self, ID: int, NAME: str, Product_ID: int, TITLE: str, DESCRIPTION: str, PRICE: float, STOCK: int):
        """
        Add one record to Product_SKUs

        Accept: (dict) {"ID": ?, "NAME": ?, "PRODUCT_ID": ?, "TITLE": ?, "DESCRIPTION": ?, "PRICE": ?,  "STOCK": ?}
        """
        # Accept dict only 
        self.cursor.execute("""
                            INSERT INTO PRODUCT_SKUS (ID, NAME, PRODUCT_ID, TITLE, DESCRIPTION, PRICE, STOCK)
                            VALUES (:ID, :NAME, :PRODUCT_ID, :TITLE, :DESCRIPTION, :PRICE, :STOCK)
                            """, ID=ID, NAME=NAME, PRODUCT_ID=PRODUCT_ID, TITLE=TITLE, DESCRIPTION=DESCRIPTION, PRICE=PRICE, STOCK=STOCK)
        

    def GetRecord(self, column, query):
        """
        Get one/many record(s) based on the query given (e.g. ID = 10)

        Input:
            column (str) -> A column of the table (e.g. ID, NAME)
            query (str)  -> Searching condition IN SQL FORMAT!!!!!! (e.g. ID = 10)

        Output:
            List of filtered search result
        """
        statement = f"SELECT {str(column)} FROM PRODUCT_SKUS {str(query)}"

        self.cursor.execute(statement)
       
        columns = [col[0] for col in self.cursor.description]
        self.cursor.rowfactory = lambda *args: dict(zip(columns, args))
        results =  self.cursor.fetchall()
        return results


    def DeleteRecord(self, column, query):
        """
        Delete one record from Product_SKUs

        Input:
            column (str) & query (str) -> To find the specificed record (e.g. WHERE ID = 10)
                                                                               (column)  (query)
        """

        statement = f"""DELETE FROM PRODUCT_SKUS
                        WHERE {str(column)} = {str(query)}
                     """
        self.cursor.execute(statement)



    def UpdateRecord(self, Column_to_be_Updated, value, Selected_Column, Target_Column) -> None:
        """
        Update a record 
        Accept: Column_to_be_Updated (str), value (any kind), Selected_Column (str), Target_Column (str)
        """
        self.cursor.execute("""
                            UPDATE PRODUCT_SKUS
                            SET :Column_to_be_Updated = :value
                            WHERE :Selected_Column = :Target_Column
                            """,  Column_to_be_Updated = Column_to_be_Updated, value=value, Selected_Column=Selected_Column, Target_Column=Target_Column)


    def ReturnNumberOfEntries(self):
        NumberOfEntries = self.cursor.execute("SELECT COUNT(*) FROM PRODUCT_SKUS")
        return NumberOfEntries