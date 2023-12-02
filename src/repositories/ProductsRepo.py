from models.Products import ProductModel

class ProductsRepository:

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
        

    def GetRecord(self, column: str, query: str) -> ProductModel:
        """
        Get one/many record(s) based on the query given (e.g. PRICE > 10)

        Input:
            column (str) -> A column of the table (e.g. ID, CATEGORY_ID, TITLE, ...)
            query (str)  -> Searching condition IN SQL FORMAT!!!!!! (e.g. PRICE > 10) or sorting method (ORDER BY)

        Output:
            List of filtered search result
        """

        # For some unknown reason, you can't use bind variables like this:

        # self.cursor.execute("""
        #                     SELECT :column FROM PRODUCTS :query
        #                     """, column=column, query=query)


        statement = f"SELECT {str(column)} FROM PRODUCTS {str(query)}"

        self.cursor.execute(statement)

        columns = [col[0] for col in self.cursor.description]
        self.cursor.rowfactory = lambda *args: dict(zip(columns, args))

        results =  self.cursor.fetchall()
        return results



    def DeleteRecord(self, column, query):
        """
        Delete one record from Products

        Input:
            column (str) & query (str) -> To find the specificed record (e.g. WHERE ID = 10)
                                                                               (column)  (query)
        """

        statement = f"""DELETE FROM PRODUCTS
                        WHERE {str(column)} = {str(query)}
                     """
        self.cursor.execute(statement)



    def UpdateRecord(self, Column_to_be_Updated, value, Selected_Column, Target_Column) -> None:
        """
        Update a record 
        Accept: Column_to_be_Updated (str), value (any kind), Selected_Column (str), Target_Column (str)
        """
        self.cursor.execute("""
                            UPDATE PRODUCTS
                            SET :Column_to_be_Updated = :value
                            WHERE :Selected_Column = :Target_Column
                            """,  Column_to_be_Updated = Column_to_be_Updated, value=value, Selected_Column=Selected_Column, Target_Column=Target_Column)


    def ReturnNumberOfEntries(self):
        NumberOfEntries = self.cursor.execute("SELECT COUNT(*) FROM PRODUCTS")
        return NumberOfEntries