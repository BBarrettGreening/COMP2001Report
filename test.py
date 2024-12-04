import pyodbc

conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=dist-6-505.uopnet.plymouth.ac.uk;"
    "DATABASE=COMP2001_BBarrettGreening;"
    "UID=BBarrettGreening;"
    "PWD=OoxR792+;"
    "TrustServerCertificate=yes;"
    "Encrypt=yes;"
)

try:
    conn = pyodbc.connect(conn_str)
    print("Connection successful!")
except Exception as e:
    print("Connection failed:", e)
