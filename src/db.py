import oracledb
from repositories.ProductsRepo import ProductsRepository
import OracleAccount

# Docs for oracledb
# https://python-oracledb.readthedocs.io/en/latest/index.html

class DatabaseConnection:

    def __init__(self):
        self.__pool:         object
        self.__connection:   object
        self.__cursor:       object

    def connect_to_DB(self):
        PolyOracle = oracledb.ConnectParams(host="studora.comp.polyu.edu.hk", port=1521, sid="dbms")
        dsn = PolyOracle.get_connect_string()
        self.__pool = oracledb.create_pool(user=OracleAccount.Oracle_Database_Account_Username,
                                         password=OracleAccount.Oracle_Database_Account_Password,
                                         dsn=dsn,
                                         encoding="UTF-8",
                                         min=2, max=5, increment=1,
                                         threaded=True)


        self.__connection = self.__pool.acquire()
        self.__cursor = self.__connection.cursor()
        print("Connected to Oracle database.")
        # a = ProductRepository(connection, connection.cursor())
        # a.AddRecord(500, 0, "TEST", "null", "???", 499)
        # a.Commit()


    def release_connection(self):
        # When your application has finished performing all required database operations, 
        # the pooled connection should be released to make it available for other users of the pool. 

        self.__pool.release(self.__connection)


    def close_all_connections(self):
        # At application shutdown, the connection pool can be completely closed using 
        self.__pool.close()



# getters
    @property
    def pool(self):
        return self.__pool

    @property
    def connection(self):
        return self.__connection

    @property
    def cursor(self):
        return self.__cursor
