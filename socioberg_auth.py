import sqlite3
from flask import render_template,redirect,request,url_for,json,session


def loginout(app):



    @app.route('/',methods=['GET','POST'])
    def home():
        
        if 'username' in session:
            return render_template('app.html',name='home')
        

        else:
            return login()



    @app.route('/signup',methods=['GET','POST'])
    def signup():
        if 'username' in session:
            return redirect(url_for('home'))

        if request.form.get('username'):
            username=request.form.get('username')
            email=request.form.get('email')
            password=request.form.get('password')
            print(username,email,password)
            user=socio_signup(username,email,password)
            if user =="email" or user=="username":
                return render_template('signup.html',error=user)
            session["username"]=user
            return redirect(url_for('home'))



            

    
        return render_template('signup.html')




    @app.route('/login',methods=['GET','POST'])
    def login():
        if 'username' in session:
            return redirect(url_for('home'))
        
        if request.form.get('email'):
            password=request.form.get('password')
            email=request.form.get('email')  

            user=socio_login(email,password)
            if user=="None":
                return render_template('login.html',error="Invalid Credential")
            session["username"]=user
            return redirect(url_for('home'))

            
        
        return render_template('login.html')


    @app.route('/logout')
    def logout():
        # Clear the session to destroy it
        session.clear()
        return redirect(url_for('home'))
















def socio_signup(username,email,password):

    try:
        connection = sqlite3.connect('socioberg_user.db')
        cursor = connection.cursor()

        # Use a parameterized query to avoid SQL injection
        query = "INSERT INTO users (username, email, password) VALUES (?, ?, ?);"
        cursor.execute(query, (username, email, password))

        # Commit the changes to the database
        connection.commit()
        return username

    except sqlite3.Error as error:
        print("SQLite error:", error.args[0].split(':')[1])
        if error.args[0].split(':')[1]=='users.username':
            return "username"
        elif error.args[0].split(':')[1]=="users.email":
            return "email"
        

    finally:
        # Close the connection in the finally block to ensure it's closed regardless of whether an exception occurred
        if connection:
            connection.close()
        


def socio_login(email,password):
        
    
    connection = sqlite3.connect('socioberg_user.db')
    cursor = connection.cursor()

    query = "SELECT username FROM users WHERE email = '"+email+"' AND password = '"+password+"'"
    cursor.execute(query)
    result = cursor.fetchone()


    connection.commit()

    if result==None:
        return("None")
    else:
        return(result[0])

    
