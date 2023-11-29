import cx_Oracle

userpwd = "cqpncltc" # Obtain password string from a user prompt or environment variable

poly = cx_Oracle.makedsn("studora.comp.polyu.edu.hk", 1521, sid="DBMS")

connection = cx_Oracle.connect(user="\"22081384d\"@dbms", password=userpwd,
                               dsn=poly,
                               encoding="UTF-8")

print("Successfully connected to Oracle Database")

