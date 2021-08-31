from authlib.integrations.flask_client import OAuth, OAuthError
from flask import Flask, url_for, redirect
from flask import session


app = Flask(__name__)
app.secret_key = 'secret'
app.config.from_object('config')

oauth = OAuth(app)
oauth.register(
    name='plazmix',
    api_base_url='https://api.plazmix.net/v1/',
    access_token_url='https://api.plazmix.net/v1/Oauth2.accessToken',
    authorize_url='https://auth.plazmix.net/oauth2/authorize'
)c


@app.errorhandler(OAuthError)
def handle_error(error):
    return error.description


@app.route('/')
def homepage():
    user = session.get('user')
    return f"Plazmix user data: {user}"


@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return oauth.plazmix.authorize_redirect(redirect_uri)


@app.route('/oauth')
def authorize():
    token = oauth.plazmix.authorize_access_token()
    resp = oauth.plazmix.get('User.me', token=token).json()
    session['user'] = resp
    return redirect(url_for('homepage'))


@app.route('/logout')
def logout():
    session.pop('token', None)
    session.pop('user', None)
    return redirect(url_for('homepage'))


if __name__ == '__main__':
    app.run()
