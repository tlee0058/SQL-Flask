from flask import Flask, render_template, redirect, request, session, flash
app = Flask(__name__)
from mysqlconnection import MySQLConnector
mysql = MySQLConnector(app, 'validation')
app.secret_key = "secret"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods =['POST'])
def add():
    
    address = request.form['email']
    print address
    query="INSERT INTO emails (address, created_at, updated_at) VALUES (:address, NOW(), NOW())"
    data = {
        'address' : address,
    }
    mysql.query_db(query, data)
    flash("Email added")
    return redirect ('/')
    
@app.route('/validate', methods =['POST'])
def validate():
        session['email'] = request.form['email']
        
        query="SELECT * FROM emails WHERE address = :address LIMIT 1"
        data = {'address': session['email']}        
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
    id_query = "SELECT id FROM emails WHERE address = :address"
    id_data = {
        'address' : session['email'],
    }
    id = mysql.query_db(id_query, id_data)
  
    return render_template('success.html', emails = emails, id = id)

@app.route('/delete/<id>')
def delete(id):
    
    query="DELETE FROM emails WHERE id = :id"
    data = {
        'id' : id,
    }
    mysql.query_db(query, data)
   


    return render_template('success.html')

app.run(debug=True)
