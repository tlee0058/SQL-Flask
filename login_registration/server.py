from flask import Flask, render_template, redirect, request, session, flash
app = Flask(__name__)
app.secret_key = "secret"
import re, md5
from mysqlconnection import MySQLConnector
mysql = MySQLConnector(app, 'logreg')

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/register', methods=['POST'])
def register():
    error = False
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    confirm_pw = request.form['confirm_pw']

    if len(first_name) < 1:
        flash("First Name has to be at least 2 character")
        error = True
    
    elif not first_name.isalpha():
        flash("First Name cannot be numbers")
        error = True
    
    if len(last_name) < 1:
        flash("Last name has to be at least 2 characters")
        error = True
    elif not last_name.isalpha():
        flash("Last name cannot be numbers")
        error = True

    if not EMAIL_REGEX.match(email):
        flash("Invalid Email")
        error = True
    
    if len(password) < 8:
        flash("Password must be at least 8 characters")
        error = True

    if confirm_pw != password:
        flash("Passwords do not match")
        error = True
    
    if error:
        return redirect ('/')

    else:
        hashed_pw = md5.new(password).hexdigest()
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (:first_name, :last_name, :email, :hashed_pw, NOW(), NOW())"
        data = {
            'first_name' : first_name,
            'last_name' : last_name,
            'email' : email,
            'hashed_pw' : hashed_pw,
        }
        record = mysql.query_db(query, data)
        print record
        return redirect ('/success')

@app.route('/success')
def success():
    
    return render_template('success.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    query = "SELECT * FROM users WHERE users.email = :email LIMIT 1" ##
    data = {
        'email' : email,
    }
    validate = mysql.query_db(query, data)
    if len(validate) != 0:
        encrypted_pw = md5.new(password).hexdigest()
        if encrypted_pw == validate[0]['password']:
            return redirect ('/success')

    else: 
        flash("invalid login")
        return redirect ('/')


    

app.run(debug=True)