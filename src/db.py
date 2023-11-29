import cx_Oracle
from cx_Oracle import Connection, SessionPool

from src import OracleAccount


def create_connection_pool() -> SessionPool:
    return cx_Oracle.SessionPool(user=OracleAccount.Oracle_Database_Account_Username,
                                 password=OracleAccount.Oracle_Database_Account_Password,
                                 dsn=cx_Oracle.makedsn("studora.comp.polyu.edu.hk", 1521, sid="dbms"),
                                 encoding="UTF-8",
                                 min=2, max=5, increment=1,
                                 threaded=True)


def get_connection() -> Connection:
    return pool.acquire()


def return_connection(conn: Connection):
    pool.release(conn)


def close_all_connections():
    pool.close()


pool = create_connection_pool()
