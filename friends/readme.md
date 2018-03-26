Let's create a very simple webpage where we can track all of our friends! We will implement the functionality to add friends and view friends through the website. All friends will be stored in the database. For this application, we won't have login/registration.

First, create your database using the following sql file: friends.sql

And consider the following ERD:
![alt tag](https://user-images.githubusercontent.com/32435667/37926240-d0d24be2-3104-11e8-8893-37320ab7ac0e.png)
Now let's start creating our sample application.

As always we will start with our server.py file. Let's first make the app work with hard coded data and then we will add the back end.

For your file structure make sure that, in addition to your server.py file, you have the mysqlconnection.py file and a templates folder with an index.html file.

Call your project "friends".