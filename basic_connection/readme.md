First, create a database called "mydb" that has a users table with a name field. Add 2-3 users using MySQLWorkbench so that you can test out the connection.

Now create a new project called "flask_mysql" and create a server.py file and a mysqlconnection.py file. 
mysqlconnection.py will be the file that connects to MySQL using the MySQL-python module we installed earlier

/mysqlconnection.py

And
/server.py

Note that we are not handling any routes on our server.py file. Instead, when we run "python server.py" we should see our users printed to the terminal.

First, run the application to make sure that you are getting your users from the database. 

Things to know about the connection:
Read all of the comments in the connection file to fully understand what is going on. Note that you don't need to know how to create one of these files -- instead, you should know how to use the file and by the end of the bootcamp, you will be experienced enough to create your own connection files.

