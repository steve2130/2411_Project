import oracledb
from repositories.ProductsRepo import ProductRepository
import OracleAccount

# Docs for oracledb
# https://python-oracledb.readthedocs.io/en/latest/index.html

class DatabaseConnection:

    pool = object
    connection = object
    cursor = object

    def connect_to_DB(self):
        PolyOracle = oracledb.ConnectParams(host="studora.comp.polyu.edu.hk", port=1521, sid="dbms")
        dsn = PolyOracle.get_connect_string()
        self.pool = oracledb.create_pool(user=OracleAccount.Oracle_Database_Account_Username,
                                         password=OracleAccount.Oracle_Database_Account_Password,
                                         dsn=dsn,
                                         encoding="UTF-8",
                                         min=2, max=5, increment=1,
                                         threaded=True)


        self.connection = self.pool.acquire()
        self.cursor = self.connection.cursor()
        print("Connected to Oracle database.")
        # a = ProductRepository(connection, connection.cursor())
        # a.AddRecord(500, 0, "TEST", "null", "???", 499)
        # a.Commit()


    def release_connection(self):
        # When your application has finished performing all required database operations, 
        # the pooled connection should be released to make it available for other users of the pool. 

        self.pool.release(self.connection)


    def close_all_connections(self):
        # At application shutdown, the connection pool can be completely closed using 
        self.pool.close()
