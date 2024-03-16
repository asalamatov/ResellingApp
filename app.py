from flask import Flask, render_template, request, redirect, flash, url_for,abort,session,appcontext_popped
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin, LoginManager, login_user, current_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from flask_admin import Admin, expose
from flask_admin.contrib.sqla import ModelView
from forms import RegistrationForm, LoginForm,PasswordResetRequestForm, ResetPasswordForm
from scripty import whole_function
from flask_mail import Mail,Message
from itsdangerous import URLSafeTimedSerializer as Serializer
from itsdangerous import BadSignature
import pyrebase
import firebase_admin
from firebase_admin import credentials,auth as admin_auth
from authlib.integrations.flask_client import OAuth
import json,binascii,os
from http.server import HTTPServer, SimpleHTTPRequestHandler
import mimetypes

# PORT = 5000

# # Update the MIME type for JavaScript files
# mimetypes.add_type('application/javascript', '.js')

# class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
#     def end_headers(self):
#         # Include additional headers here if needed
#         SimpleHTTPRequestHandler.end_headers(self)

# httpd = HTTPServer(("", PORT), CustomHTTPRequestHandler)

# print(f"Serving at port {PORT}")
# httpd.serve_forever()



app = Flask(__name__)


appConf = {
        "OAUTH2_CLIENT_ID": "4977128071-n6ct24l70pu4h2ps83f51rttasikk90v.apps.googleusercontent.com",
        "OAUTH2_CLIENT_SECRET": "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",
        "OAUTH2_META_URL": "https://accounts.google.com/.well-known/openid-configuration",
        "FLASK_SECRET": "232d15f0-36bc-49d3-ae3f-b9daef5bb29f",

}
app.secret_key = appConf.get("FLASK_SECRET")

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


@app.route('/h')
def homee():
    return render_template('son.html')



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



app.config['SECRET_KEY'] = 'moma4539'

@login_manager.user_loader
def load_user(user_id):
    try:
        # Check if user_id is None or an empty string
        if user_id is None or user_id == '':
            return None
        return User.query.get(int(user_id))
    except ValueError:
        # Handle the case where user_id cannot be converted to an integer
        return None



@app.route("/useraccount", methods=['GET', 'POST'])
def useraccount():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Register':
            email = request.form['email']
            password = request.form['password']
            try:
                auth.create_user_with_email_and_password(email, password)
                flash('Account created successfully!', 'success')
                return redirect(url_for('user_account'))
            except Exception as e:
                flash('Account creation failed: ' + str(e), 'danger')
        elif request.form['submit_button'] == 'Login':
            email = request.form['email']
            password = request.form['password']
            try:
                auth.sign_in_with_email_and_password(email, password)
                user = User(email=email)  # Dummy User object since we don't have a User model
                login_user(user)
                flash('Login successful!', 'success')
                return redirect("/getoffer")
            except Exception as e:
                flash('Login failed: ' + str(e), 'danger')

    return render_template('son.html')

# @app.route("/useraccount", methods=['GET', 'POST'])
# def user_account():
#     if 'user' in session:
#         return redirect(url_for('getoffer'))
    
#     else:
#         if request.method == 'POST':
#             email = request.form.get('email')
#             password = request.form.get('password')
#             action = request.form.get('action')

#             if action == 'login':
#                 try:
#                     user = auth.sign_in_with_email_and_password(email, password)
#                     session['user'] = email
#                     return redirect("/getoffer")
#                 except:
#                     flash('Login failed. Please check your credentials and try again.', 'danger')
#             elif action == 'signup':
#                 try:
#                     user = auth.create_user_with_email_and_password(email, password)
#                     session['user'] = email
#                     flash('Account created successfully. Please log in.', 'success')
#                     return redirect(url_for('user_account'))
#                 except:
#                     flash('Email already exists. Please try another one.', 'danger')
    
#     return render_template("useraccount.html")


@app.route("/logout")
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect("/useraccount")
cred = credentials.Certificate("C:\\Users\\omerb\\Dropbox\\PC\\Downloads\\first-b689f-firebase-adminsdk-675xy-5f4c0998c0.json")
firebase_admin.initialize_app(cred)

@app.route('/google_sign_in', methods=['POST'])
def google_sign_in():
    # Get the ID token sent by the client
    id_token = request.json.get('idToken')
    # Verify the ID token and retrieve the user's Firebase ID
    decoded_token = admin_auth.verify_id_token(id_token)
    uid = decoded_token['uid']
    # Proceed with your user handling logic, e.g., creating a user record in your database if it doesn't exist
    return redirect(url_for('getoffer'))

    return 'User authenticated', 200

@app.route('/admin/users')
@login_required
def list_users():

    if not current_user.is_admin:  # Assuming you have an is_admin attribute or similar
        return abort(403)
    users = User.query.all()
    return render_template('list_users.html', users=users)

# Initialize an empty shopping cart
shopping_cart = []

@app.route("/")
@app.route("/homepage")
def index():
    return render_template("lindex.html",session=session.get("user"),pretty=json.dumps(session.get("user"),indent=4))
    

@app.route("/getoffer", methods=["GET", "POST"])
def getoffer():
    # Initialize an empty shopping cart if not defined
    if 'shopping_cart' not in globals():
        global shopping_cart
        shopping_cart = []
        
    if request.method == "POST":
        # Check if 'isbn' key exists in form data
        if 'isbn' in request.form:
            user_isbn = request.form["isbn"]
            Isbnumber = user_isbn
            quantity = int(request.form.get("quantity", 1))  # Get quantity from the form

            # Call the function to get the offer and item details
            total_earnings, item_name, Isbnumber, _, first_image_link = whole_function(Isbnumber, quantity)  # Ignore the quantity returned by whole_function

            # Find the index of the item in the shopping cart
            item_index = next((index for index, item in enumerate(shopping_cart) if item[2] == Isbnumber), None)

            if item_index is not None:
                # Update the quantity and initial earnings for the item
                _, _, _, initial_quantity, _, _ = shopping_cart[item_index]
                initial_earnings = total_earnings / initial_quantity  # Calculate the initial earnings per item

                # Update the item in the shopping cart
                shopping_cart[item_index] = (total_earnings, item_name, Isbnumber, quantity, first_image_link, initial_earnings)

                # Delete the item from the shopping cart if quantity is 0
                if quantity == 0:
                    shopping_cart = [(earnings, name, isbn, quantity, img_link, initial_earnings) for earnings, name, isbn, quantity, img_link, initial_earnings in shopping_cart if isbn != Isbnumber]

            else:
                if quantity != 0:  # Check if quantity is not zero before performing the division
                    # Add the item to the shopping cart
                    initial_earnings = total_earnings / quantity  # Calculate the initial earnings per item
                    shopping_cart.append((total_earnings, item_name, Isbnumber, quantity, first_image_link, initial_earnings))
        action = request.form.get("action")  # Get the value of the "action" parameter
            # Check for "Empty Cart" action
        if action == "empty_cart":
            shopping_cart = []  # Empty the shopping cart
    
    total_values = sum(item[0] for item in shopping_cart)
    total_quantities = sum(item[3] for item in shopping_cart)  # Calculate the total earnings with current quantities
    
    return render_template("index.html", shopping_cart=shopping_cart, total_values=total_values,total_quantities=total_quantities)
def assign_admin_role():
    user = User.query.filter_by(email='03omerbar@gmail.com').first()
    if user and not user.is_admin:
        user.is_admin = True
        db.session.commit()
        print(f"Assigned admin role to {user.email}")
    elif user:
        print(f"{user.username} is already an admin.")
    else:
        print("User 'mbappe' not found.")
if __name__ == "__main__":
    with app.app_context():
        assign_admin_role()
    app.run(debug=True)
