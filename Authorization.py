# facebook_auth.py
from flask import redirect, url_for, session, request,render_template
from flask_oauthlib.client import OAuth
from db_handler import*

def create_facebook_oauth(app):
    oauth = OAuth(app)

    facebook = oauth.remote_app(
        'facebook',
        consumer_key=1392141388101711,
        consumer_secret='bf1260d487a10744bf2aa02eb24326c5',
        request_token_params={'scope': 'read_insights,pages_manage_cta,pages_show_list,business_management,instagram_basic,instagram_manage_comments,instagram_manage_insights,instagram_content_publish,pages_read_engagement,pages_manage_metadata,pages_read_user_content,pages_manage_posts,instagram_manage_events,,page_events,pages_messaging,pages_messaging_subscriptions,instagram_manage_messages'},
        base_url='https://graph.facebook.com/',
        request_token_url=None,
        access_token_url='/oauth/access_token',
        authorize_url='https://www.facebook.com/v13.0/dialog/oauth',
    )

    @app.route('/facebook-login')
    def facebook_login():
        return facebook.authorize(callback=url_for('facebook_authorized', _external=True))

    @app.route('/facebook-login/authorized')
    def facebook_authorized():
        response = facebook.authorized_response()
        if response is None or response.get('access_token') is None:
            return 'Access denied: reason={} error={}'.format(
                request.args['error_reason'],
                request.args['error_description']
            )
        session['facebook_token'] = response['access_token']

        user_info = facebook.get('me/accounts?fields=id,name,picture')
        pages={}

        for page in user_info.data['data']:
            pages[page['id']]= [page['name'],page['picture']['data']['url'] ]

        return render_template('app.html',name='addAccount',pages=pages,popup="showlist")
    


    @app.route('/process_page_selection', methods=['POST'])
    def process_page_selection():
        selected_page_id = request.form.get('data')
        session['facebook_page']=selected_page_id
        insta = facebook.get(selected_page_id+'?fields=instagram_business_account')

        session['instagram_id']=insta.data['instagram_business_account']['id']


        save_token(forApp="facebook",username=session['username'],token=session['facebook_token'],page=session['facebook_page']) 
        save_token(forApp="instagram",username=session['username'],token=session['facebook_token'],page=session['instagram_id']) 


        return redirect(url_for('addAccount'))



    @facebook.tokengetter
    def get_facebook_oauth_token():
        return session.get('facebook_token')

    return facebook
