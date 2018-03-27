from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
app.secret_key = "secret"
mysql = MySQLConnector(app, 'mydb')

@app.route('/')
def index():
    query = "SELECT name, age, DATE_FORMAT(created_at, '%M %D') AS 'since', DATE_FORMAT(created_at, '%Y') as 'year' FROM full_friends"
    friends = mysql.query_db(query)
    return render_template('index.html', all_friends = friends)

@app.route('/add', methods=['POST'])
def create():
    name = request.form['name']
    age = request.form['age']
    
    query="INSERT INTO full_friends (name, age, created_at, updated_at) VALUES (:name, :age, NOW(), NOW())"
    data = {
        'name' : name,
        'age' : age,
  
    }
    mysql.query_db(query,data)

    return redirect ('/')

app.run(debug=True) 