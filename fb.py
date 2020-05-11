import fdb

con = fdb.connect(dsn='localhost:axioma', user='sysdba', password='masterke')

# Create a Cursor object that operates in the context of Connection con:
cur = con.cursor()

# Execute the SELECT statement:
cur.execute("select first 10 * from assortment")

# Retrieve all rows as a sequence and print that sequence:
print(cur.fetchall())