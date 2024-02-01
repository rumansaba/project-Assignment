from flask import Flask, render_template, redirect, url_for, session
from flask_oauthlib.client import OAuth
from werkzeug.urls import url_quote as url_quote

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key

# Configure OAuth for Google
oauth = OAuth(app)
google = oauth.remote_app(
    'google',
    consumer_key='YOUR_GOOGLE_CLIENT_ID',
    consumer_secret='YOUR_GOOGLE_CLIENT_SECRET',
    request_token_params={
        'scope': ('email', 'profile'),
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

# Configure OAuth for Facebook
facebook = oauth.remote_app(
    'facebook',
    consumer_key='YOUR_FACEBOOK_APP_ID',
    consumer_secret='YOUR_FACEBOOK_APP_SECRET',
    request_token_params={
        'scope': ['email'],
    },
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_method='GET',
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
)

@app.route('/')
def index():
    return render_template('index.html', user=session.get('user'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login/google')
def login_google():
    return google.authorize(callback=url_for('authorized', _external=True, _scheme='https', provider='google'))

@app.route('/login/facebook')
def login_facebook():
    return facebook.authorize(callback=url_for('authorized', _external=True, _scheme='https', provider='facebook'))

@app.route('/logout')
def logout():
    session.pop('google_token', None)
    session.pop('facebook_token', None)
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/login/authorized/<provider>')
def authorized(provider):
    response = None
    try:
        if provider == 'google':
            response = google.authorized_response()
            session['google_token'] = (response['access_token'], '')
            user_info = google.get('userinfo')
        elif provider == 'facebook':
            response = facebook.authorized_response()
            session['facebook_token'] = (response['access_token'], '')
            user_info = facebook.get('me?fields=id,name,email')

        session['user'] = {'id': user_info.data['id'], 'name': user_info.data['name'], 'email': user_info.data.get('email', '')}
    except Exception as e:
        print(str(e))

    return redirect(url_for('index'))

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('facebook_token')

if __name__ == '__main__':
    app.run(host="0.0.0.0")
