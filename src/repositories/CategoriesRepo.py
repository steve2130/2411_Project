from models.Categories import CategoriesModel

class CategoriesRepository:

    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor


    def Commit(self):
        """
        Upload the changes to database
        """
        self.connection.commit()


    def AddRecord(self, ID: int, NAME: str):
        """
        Add one record to Categories

        Accept: (dict) {"ID": ?, "NAME": ?}
        """
        # Accept dict only 
        self.cursor.execute("""
                            INSERT INTO Categories (ID, NAME)
                            VALUES (:ID, :NAME)
                            """, entity.to_db)
        

    def GetRecord(self, column: str, query: str) -> CategoriesModel:
        """
        Get one/many record(s) based on the query given (e.g. ID = 10)

        Input:
            column (str) -> A column of the table (e.g. ID, NAME)
            query (str)  -> Searching condition IN SQL FORMAT!!!!!! (e.g. ID = 10)

        Output:
            List of filtered search result
        """
        statement = f"SELECT {str(column)} FROM CATEGORIES {str(query)}"

        self.cursor.execute(statement)

        columns = [col[0] for col in self.cursor.description]
        self.cursor.rowfactory = lambda *args: dict(zip(columns, args))
        results =  self.cursor.fetchall()
        return results


    def DeleteRecord(self, column, query):
        """
        Delete one record from Categories

        Input:
            column (str) & query (str) -> To find the specificed record (e.g. WHERE ID = 10)
                                                                               (column)  (query)
        """

        statement = f"""DELETE FROM CATEGORIES
                        WHERE {str(column)} = {str(query)}
                     """
        self.cursor.execute(statement)



    def UpdateRecord(self, ID: int, NAME: str) -> None:
        """
        Update a record (searched with ID) with the changed attribute (change with setter in Categories.py)

        Input: ID (int), NAME (str)
        """
        self.cursor.execute("""
                            UPDATE CATEGORIES
                            SET :NAME
                            WHERE :ID
                            """, NAME=NAME, ID=ID)


    def ReturnNumberOfEntries(self):
        NumberOfEntries = self.cursor.execute("SELECT COUNT(*) FROM CATEGORIES")
        return NumberOfEntries