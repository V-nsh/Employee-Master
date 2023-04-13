# from dbm import _Database
from sqlite3 import IntegrityError
import requests
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host = "127.0.0.1",
    port = "3306",
    database = "employeeMaster",
    user= "root",
    password = "password",
)

"""
Database Name: employeeMaster
Running it on localhost so I am sharing the schema 

employees table:
CREATE TABLE employees(name varchar(100), id int NOT NULL PRIMARY KEY, role varchar(100), contact int, address varchar(255));
"""

cursor = db.cursor()

cursor.execute('SET autocommit=0')

print(db)
msg = ''
@app.route('/')
def main():
    return render_template('home.html')

@app.route('/insert', methods=['GET','POST'])
def insert():
    if request.method == 'POST':
        try:
            n = request.form['name1']
            i = request.form['id1']
            r = request.form['role']
            c = request.form['contact']
            a = request.form['address']
            cursor.execute('INSERT INTO employees (name, id, role, contact, address) VALUES (%s, %s, %s, %s, %s)', (n, i, r, c, a))
            # db.commit()
            # return redirect(url_for("insert"))
        except mysql.connector.errors.IntegrityError:
            error = 'Primary key must be unique!'
            return render_template("insert.html", key_error = error)
    return render_template("insert.html")

@app.route('/commit', methods = ['GET', 'POST'])
def commit():
    db.commit()
    return redirect(url_for("main"))

@app.route('/modify', methods = ['GET', 'POST'])
def modify():
    if request.method =='POST':
        n = request.form['name1']
        i = request.form['id1']
        r = request.form['role']
        c = request.form['contact']
        a = request.form['address']
        cursor.execute('UPDATE employees SET name = %s, role = %s, contact = %s, address = %s WHERE id = %s', (n, r, c, a, i))
        # db.commit()
        # return redirect(url_for("modify"))
    return render_template('modify.html')

@app.route('/undo', methods = ['GET', 'POST'])
def undo():
    db.rollback()
    return render_template('home.html')

@app.route('/delete', methods = ['GET', 'POST'])
def delete():
    if request.method == 'POST':
        i = request.form['id1']
        cursor.execute('DELETE FROM employees WHERE id = %s', (i,))
        # db.commit()
        # return redirect(url_for("delete"))
    return render_template('delete.html')

if __name__=="__main__":
    app.run(debug = True)