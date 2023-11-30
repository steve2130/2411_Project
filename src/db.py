import oracledb
from repositories.ProductsRepo import ProductRepository
import OracleAccount


def connect_to_DB():
    print("in db")

    PolyOracle = oracledb.ConnectParams(host="studora.comp.polyu.edu.hk", port=1521, sid="dbms")
    dsn = PolyOracle.get_connect_string()
    pool = oracledb.create_pool(user=OracleAccount.Oracle_Database_Account_Username,
                                password=OracleAccount.Oracle_Database_Account_Password,
                                dsn=dsn,
                                encoding="UTF-8",
                                min=2, max=5, increment=1,
                                threaded=True)

    print("Connected.")
    connection = pool.acquire()
    # a = ProductRepository(connection, connection.cursor())
    # a.AddRecord(500, 0, "TEST", "null", "???", 499)
    # a.Commit()

    return connection, connection.cursor()


# def return_connection(conn: Connection):
#     pool.release(conn)


# def close_all_connections():
#     pool.close()

