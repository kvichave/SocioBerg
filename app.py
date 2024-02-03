from flask import Flask,render_template,redirect,request,url_for,json,session
from flask_oauthlib.client import OAuth
from credentials import CLIENT_ID,CLIENT_SECRET
import sqlite3,db_handler
import requests
from socioberg_auth import socio_signup,socio_login,loginout
from Authorization import create_facebook_oauth


app = Flask(__name__)
app.secret_key = CLIENT_SECRET  # Replace with a secure secret key
app.config['PERMANENT_SESSION_LIFETIME'] = 10 * 365 * 24 * 60 * 60  # 10 years in seconds




loginout(app)

facebook=create_facebook_oauth(app)







@app.route('/addAccount')
def addAccount():


    # for instagram
    db_handler.retrive_token(username=session['username'],forApp='instagram')

    if 'instagram_id' in session:

        instagram_data=facebook.get(session['instagram_id']+'?fields=id,username,name,profile_picture_url')
    
    else:
        instagram_data=''
        


    
    
    
    return render_template('app.html',name='addAccount',instagram_data=instagram_data)

    
@app.route('/checkapp/<appName>')
def checkapp(appName):

    if appName=='instagram':
        if'instagram_id' not in session:
            print('inside facebookt token')
            token=db_handler.retrive_token(username=session['username'],forApp='instagram')
            if token =='None':
                print('inside  if')

                return redirect(url_for('facebook_login'))
            
        

        return redirect(url_for('addAccount'))
        


        

@app.route('/page-selection/<popup>/<pages>')
def page_selection(popup,pages):

    return render_template('app.html',popup=popup,name='addAccount',pages=pages)








@app.route('/remove/<id>')
def remove(id):
    db_handler.delete(session['username'],id)
    session.pop('instagram_id', None)

    return redirect(url_for('addAccount'))



if __name__ == '__main__':
    app.run(ssl_context='adhoc',debug=True)