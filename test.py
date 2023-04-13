import mysql.connector

db = mysql.connector.connect(
    host = "127.0.0.1",
    port = "3306",
    database = "employeeMaster",
    user= "root",
    password = "password",
    # database = "Employee_Master"
)

cursor = db.cursor()
query = "SELECT * FROM employees "
cursor.execute(query)
print(db)

records = cursor.fetchall()
for row in records:
    print(row)