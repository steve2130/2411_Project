import oracledb
from oracledb import Connection

from src import OracleAccount


def create_connection_pool():
    return oracledb.create_pool(user=OracleAccount.Oracle_Database_Account_Username,
                                password=OracleAccount.Oracle_Database_Account_Password,
                                dsn=oracledb.makedsn("studora.comp.polyu.edu.hk", 1521, sid="dbms"),
                                encoding="UTF-8",
                                min=2, max=5, increment=1,
                                threaded=True)


def get_connection():
    return pool.acquire()


def return_connection(conn: Connection):
    pool.release(conn)


def close_all_connections():
    pool.close()


pool = create_connection_pool()
