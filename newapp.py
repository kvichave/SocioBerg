
from flask import Flask, redirect, url_for, session,request,render_template
from flask_oauthlib.client import OAuth

app = Flask(__name__)
app.secret_key = 'bf1260d487a10744bf2aa02eb24326c5'  # Replace with a secure secret key

oauth = OAuth(app)

facebook = oauth.remote_app(
    'facebook',
    consumer_key=1392141388101711,
    consumer_secret='bf1260d487a10744bf2aa02eb24326c5',
    request_token_params={'scope': 'read_insights,pages_manage_cta,pages_show_list,business_management,instagram_basic,instagram_manage_comments,instagram_manage_insights,instagram_content_publish,pages_read_engagement,pages_manage_metadata,pages_read_user_content,pages_manage_posts,instagram_manage_events,,page_events,pages_messaging,pages_messaging_subscriptions,instagram_manage_messages'},
    base_url='https://graph.facebook.com/',
    # redirect_uri=''
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/v13.0/dialog/oauth',
)

@app.route('/')
def index():
    return 'Welcome to the Flask Facebook Authentication App'

@app.route('/login')
def login():
    return facebook.authorize(callback='https://127.0.0.1:7000/login/authorized')

@app.route('/logout')
def logout():
    session.pop('facebook_token', None)
    return redirect(url_for('index'))

@app.route('/login/authorized')
def authorized():
    response = facebook.authorized_response()
    if response is None or response.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )
    print(get_facebook_oauth_token())
    session['facebook_token'] = (response['access_token'])
    user_info = facebook.get('me/accounts?fields=id,name')
    pages={page['id']: page['name'] for page in user_info.data['data']}
    

    return render_template('accounts.html',pages=pages)





@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('facebook_token')

if __name__ == '__main__':
    app.run(ssl_context='adhoc',debug=True,port=7000)
