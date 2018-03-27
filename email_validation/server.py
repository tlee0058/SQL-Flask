from flask import Flask, render_template, redirect, request, session, flash
app = Flask(__name__)
from mysqlconnection import MySQLConnector
mysql = MySQLConnector(app, 'mydb')
app.secret_key = "secret"



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods =['POST'])
def add():
    
        email = request.form['email']
        print email
        query="INSERT INTO emails (emails, created_at, updated_at) VALUES (:email, NOW(), NOW())"
        data = {
            'email' : email,
        }
        mysql.query_db(query, data)
        flash("Email added")
        return redirect ('/')
    
@app.route('/validate', methods =['POST'])
def validate():
        session['vemail'] = request.form['vemail']
        
        query="SELECT * FROM emails WHERE emails = :email LIMIT 1"
        data = {'email': session['vemail']}        
        check = mysql.query_db(query, data)
        if len(check) != 0:
            return redirect ('/success')
        else:
            flash("invalid email")
            return redirect ('/')

@app.route('/success')
def success():
    
    # query = ("SELECT * FROM emails WHERE emails = :email")
    # data = {
    #     'email' : session['vemail']
    # }
    emails = mysql.query_db("SELECT * FROM emails")
    
  
    return render_template('success.html', emails = emails)

@app.route('/delete/<email_id>')
def delete(email_id):
    query="DELETE FROM emails WHERE id = :email_id"
    data = {
        'email_id' : email_id,
    }
    mysql.query_db(query, data)

    return render_template('success.html')

app.run(debug=True)