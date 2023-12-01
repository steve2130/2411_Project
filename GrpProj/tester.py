import pyodbc

def connect_test_db():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;UID=sa;PWD=Test1234;TrustServerCertificate=yes')
    
    crsr = conn.cursor()
    rows = crsr.execute("SELECT TOP 1000 * FROM test.dbo.users")
    for row in rows:
        print(row)
    crsr.close()
    conn.close()

connect_test_db()
