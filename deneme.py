appConf = {
        "OAUTH2_CLIENT_ID": "4977128071-n6ct24l70pu4h2ps83f51rttasikk90v.apps.googleusercontent.com",
        "OAUTH2_CLIENT_SECRET": "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",
        "OAUTH2_META_URL": "https://accounts.google.com/.well-known/openid-configuration",
        "FLASK_SECRET": "232d15f0-36bc-49d3-ae3f-b9daef5bb29f",

}
app.secret_key = appConf.get("FLASK_SECRET")


login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)  # Add this line

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"



oauth = OAuth(app)
oauth.register("myApp",
               client_id = appConf.get("OAUTH2_CLIENT_ID"),
               client_secret = appConf.get("OAUTH2_CLIENT_SECRET"),
               server_metadata_url = appConf.get("OAUTH2_META_URL"),
               client_kwargs ={
                   "scope": "openid profile email"
               }
               
               )

@app.route("/google-login")
def googleLogin():
    return oauth.myApp.authorize_redirect(redirect_uri=url_for("googleCallback",_external = True))
@app.route("/signin-google")
def googleCallback():
    token = oauth.myApp.authorize_access_token()
    resp = oauth.myApp.get('https://www.googleapis.com/oauth2/v3/userinfo', token=token)
    user_info = resp.json()
    user_email = user_info['email']
    user_name = user_info.get('name', user_email.split('@')[0])  # Default to part of email if name not provided
    
    # Find existing user or create a new one
    user = User.query.filter_by(email=user_email).first()
    if user is None:
        user = User(username=user_name, email=user_email)
        random_password = binascii.hexlify(os.urandom(16)).decode()
        user.set_password(random_password)
        db.session.add(user)
        db.session.commit()
    
    # Log in the user
    login_user(user)
    
    # Redirect to the desired page after login
    return redirect(url_for("getoffer"))
@app.route("/google-logout")
def logout3():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect("/useraccount")

config = {
    "apiKey": "AIzaSyDB8HRp2gYjteaS4hryqzQB2fh54FDzWn0",
    "authDomain": "first-b689f.firebaseapp.com",
    "projectId" : "first-b689f",
    "storageBucket" : "first-b689f.appspot.com",
    "messagingSenderId" : "4977128071",
    "appId" : "1:4977128071:web:f816e9c1f1094020aefe22",
    "measurementId" : "G-TD7WF2EZ6X",
    "databaseURL" : " "
}

firbase = pyrebase.initialize_app(config)
auth = firbase.auth()