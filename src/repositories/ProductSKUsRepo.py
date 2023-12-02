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


    def AddRecord(self, entity=ProductSKUsModel):
        """
        Add one record to Product_SKUs

        Accept: (dict) {"ID": ?, "NAME": ?, "PRODUCT_ID": ?, "TITLE": ?, "DESCRIPTION": ?, "PRICE": ?,  "STOCK": ?}
        """
        # Accept dict only 
        self.cursor.execute("""
                            INSERT INTO PRODUCT_SKUS (ID, NAME, PRODUCT_ID, TITLE, DESCRIPTION, PRICE, STOCK)
                            VALUES (:ID, :NAME, :PRODUCT_ID, :TITLE, :DESCRIPTION, :PRICE, :STOCK)
                            """, entity.to_db)
        

    def GetRecord(self, column, query):
        """
        Get one/many record(s) based on the query given (e.g. ID = 10)

        Input:
            column (str) -> A column of the table (e.g. ID, NAME)
            query (str)  -> Searching condition IN SQL FORMAT!!!!!! (e.g. ID = 10)

        Output:
            List of filtered search result
        """
        statement = f"SELECT {str(column)} FROM PRODUCT_SKUS WHERE {str(query)}"

        self.cursor.execute(statement)
        results =  self.cursor.fetchall()
        return [result for result in results]


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



    def UpdateRecord(self, entity: ProductSKUsModel) -> None:
        """
        Update a record (searched with ID) with the changed attribute (change with setter in ProductSKUs.py)
        """
        self.cursor.execute("""
                            UPDATE PRODUCT_SKUS
                            SET :NAME, :PRODUCT_ID, :TITLE, :DESCRIPTION, :PRICE, :STOCK
                            WHERE :ID
                            """, NAME=entity.NAME, PRODUCT_ID=entity.PRODUCT_ID, TITLE=entity.TITLE, DESCRIPTION=entity.DESCRIPTION, PRICE=entity.PRICE, STOCK=entity.STOCK, ID=entity.ID)
