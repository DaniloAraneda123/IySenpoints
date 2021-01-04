import pyodbc

userName = 'prueba'
password = '123456'
nameBD = 'rastreo'
driver = '{ODBC Driver 17 for SQL Server}'
server = 'DESKTOP-ERK5868'

stringConn = 'Driver={0};Server={1};Database={2};Trusted_Connection=yes;uid={3};pwd={4}'.format(
    driver, server, nameBD, userName, password)
conn = pyodbc.connect(stringConn)
cursor = conn.cursor()

def closeConexion():
    conn.close()
