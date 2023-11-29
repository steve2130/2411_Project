import oracledb
import OracleAccount







def Oracle_Database_connection():
    connection = oracledb.connect(user=OracleAccount.Oracle_Database_Account_Username, password=OracleAccount.Oracle_Database_Account_Password,
                                host="studora.comp.polyu.edu.hk", port=1521, sid="dbms",
                                encoding="UTF-8")


    print("Successfully connected to Oracle Database")
    return connection



def main():
    connection = Oracle_Database_connection()
    cursor = connection.cursor()
    

    cursor.execute("insert into USERS values (1, 'A', 'AA', 'BB', 'N')")
    connection.commit()

    for result in cursor.execute("select * from USERS"):
        print(result)

    connection.close()

if __name__ == "__main__":
    main()
    