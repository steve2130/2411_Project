from src.db import get_connection
from src.models import Categories

class CategoriesRepository:

    def __init__(self):
        self.connection = get_connection()
        self.cursor = self.connection.cursor()


    def Commit(self):
        """
        Upload the changes to database
        """
        self.connection.commit()


    def AddRecord(self, entity=Categories):
        """
        Add one record to Categories

        Accept: (dict) {"ID": ?, "NAME": ?}
        """
        # Accept dict only 
        self.cursor.execute("""
                            INSERT INTO Categories (ID, NAME)
                            VALUES (:ID, :NAME)
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
        self.cursor.execute("""
                            SELECT :column FROM CATEGORIES
                            WHERE :query
                            """, column=column, query=query)
        results =  self.cursor.fetchall()

        return [result for result in results]


    def DeleteRecord(self, column, query):
        """
        Delete one record from Categories

        Input:
            column (str) & query (str) -> To find the specificed record (e.g. WHERE ID = 10)
                                                                               (column)  (query)
        """

        self.cursor.execute("""
                            DELETE FROM CATEGORIES
                            WHERE :column = :query
                            """, column=column, query=query)


    def UpdateRecord(self, entity: Categories) -> None:
        """
        Update a record (searched with ID) with the changed attribute (change with setter in Categories.py)
        """
        self.cursor.execute("""
                            UPDATE CATEGORIES
                            SET :NAME
                            WHERE :ID
                            """, NAME=entity.NAME, ID=entity.ID)
