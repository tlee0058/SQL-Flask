from flask import Flask, request, redirect, render_template, session, flash
app = Flask(__name__)
app.secret_key = 'ThisIsSecret'

import re, md5
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[a-zA-Z]{1,}$')
PASSWORD_REGEX = re.compile(r'^.{8,}$')
# PASSWORD_REGEX at least 8 characters /^.{8,}$/

from mysqlconnection import MySQLConnector
mysql = MySQLConnector(app,'thewall')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    errors = False
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    confirm_pw = request.form['confirm_pw']

    query = "SELECT * FROM users WHERE email = :email"
    data = {'email': email}
    if len(mysql.query_db(query, data)) == 0: #check if email is already in system first before moving on
        if not NAME_REGEX.match(first_name):
            flash("First Name cannot have numbers and must be at least 2 characters")
            errors = True
        
        if not NAME_REGEX.match(last_name):
            flash("Last name cannot have nubmers and must be at least 2 characters")
            errors = True
        

        if not EMAIL_REGEX.match(email):
            flash("Invalid email format")
            errors = True

        if not PASSWORD_REGEX.match(password):
            flash("Password must be at least 8 characters")
            errors = True
            
        if password != confirm_pw:
            flash("Passwords do not match")
            errors = True
        if errors:
            return redirect ('/')
        else: 
            hashed_pw = md5.new(password).hexdigest()
            query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (:first_name, :last_name, :email, :password, NOW(), NOW())"
            data = {
                'first_name' : first_name,
                'last_name' : last_name,
                'email' : email,
                'password' : hashed_pw,
            }
            mysql.query_db(query,data)
            user_query = "SELECT * FROM users where users.email = :email AND users.password = :password"
            query_data = {"email": email, 'password':hashed_pw}
            user = mysql.query_db(user_query, query_data)
            
            session['id'] = user[0]['id']
            session['first_name'] = user[0]['first_name']
            return redirect('/wall')
    else:
        flash("Email address is already registered or invalid")
        return redirect('/')

@app.route('/wall')
def wall():
    usermessages = mysql.query_db("SELECT CONCAT(first_name, ' ', last_name) AS full_name, message, date_format(messages.created_at, '%M %D %Y')\
                AS messagedate, messages.id FROM users\
                JOIN messages ON users.id = messages.user_id;")

    commessages = mysql.query_db("SELECT CONCAT(first_name, ' ', last_name) AS full_name, comments.message_id AS common_id, comment, messages.id AS message_id, \
        comments.id AS comment_id, date_format(comments.created_at, '%M %D %Y') AS comment_date\
        FROM messages \
        JOIN comments ON comments.message_id = messages.id\
        JOIN users ON users.id = comments.user_id")
    
    return render_template('wall.html', usermessages = usermessages, commessages = commessages)

@app.route('/post_msg', methods=['POST'])
def post_msg():
    query="INSERT INTO messages (message, created_at, updated_at, user_id) VALUES (:message, NOW(), NOW(), :user_id)"
    data = {
        'message' : request.form['message'],
        'user_id' : session['id'],
    }
    message = mysql.query_db(query, data)
    session['message_id'] = message[0]['id']
    print message
    return redirect ('/wall')

@app.route('/post_comm/<id>', methods=['POST'])
def post_comm(id):
    query = "INSERT INTO comments (message_id, user_id, comment, created_at, updated_at)\
            VALUES (:message_id, :user_id, :comment, NOW(), NOW())"
    data = {
        'message_id' : id,
        'user_id' : session['id'],
        'comment' : request.form['comment'],
    }
    mysql.query_db(query, data)
    
    
    return redirect ('/wall')

@app.route('/delete/<id>')
def delete(id):
    query = "DELETE FROM comments WHERE id = :id"
    data = {'id' : id}
    mysql.query_db(query, data)
    return redirect ('/wall')



@app.route('/login', methods=['POST'])
def login():
    query = "SELECT * FROM users WHERE email = :email LIMIT 1"
    data = {'email': request.form['email']}
    validate = mysql.query_db(query, data)
    if len(validate) == 0:
        flash("no such email")
        return redirect ('/')
    else:
        encrypted_pw = md5.new(request.form['password']).hexdigest()
        if encrypted_pw == validate[0]['password']:
            session['id'] = validate[0]['id']
            return redirect ('/wall')
            
        else:
            flash("Invalid Login")

            return redirect ('/')
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect ('/')
app.run(debug=True)