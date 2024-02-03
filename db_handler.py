import requests,json
import sqlite3 
from flask import render_template,redirect,request,url_for,json,session



def save_token(forApp,username,token,page='null'):
    connection = sqlite3.connect('socio.db')
    cursor = connection.cursor()

    # Use a parameterized query to avoid SQL injection
    query = "INSERT INTO Access_code (username, access_code, forApp,page) VALUES (?, ?, ?,?);"
    cursor.execute(query, (username, token, forApp, page))

    # Commit the changes to the database
    connection.commit()





def retrive_token(username,forApp):
    print(username)
    print(forApp)

    connection = sqlite3.connect('socio.db')
    cursor = connection.cursor()



    query = "SELECT access_code, page FROM Access_code WHERE username = '{}' AND forApp = '{}';".format(username, forApp)
    cursor.execute(query)
    # print(query)

    result = cursor.fetchall()
    connection.commit()
    # print(result)
    if result==[]:

        return 'None'

    else:
        session['facebook_token']=result[0][0]
        session['facebook_page']=result[0][1]

        return result
    


def delete(username,id):
    connection = sqlite3.connect('socio.db')

    # Create a cursor object
    cursor = connection.cursor()

    # SQL command to delete entries
    delete_query = "DELETE FROM Access_code WHERE username = ? AND page = ?;"

    # Parameters to be substituted in the query

    # Execute the query
    cursor.execute(delete_query, (username,id))

    # Commit the changes
    connection.commit()

    # Close the cursor and connection
    cursor.close()
    connection.close()
