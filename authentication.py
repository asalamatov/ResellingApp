import pyrebase

config = {
    "apiKey": "AIzaSyDB8HRp2gYjteaS4hryqzQB2fh54FDzWn0",
    "authDomain": "first-b689f.firebaseapp.com",
    "projectId" : "first-b689f",
    "storageBucket" : "first-b689f.appspot.com",
    "messagingSenderId" : "4977128071",
    "appId" : "1:4977128071:web:f816e9c1f1094020aefe22",
    "measurementId" : "G-TD7WF2EZ6X",
    "databaseURL" : ""
}

firbase = pyrebase.initialize_app(config)
auth = firbase.auth()

email = 'test@gmail.com'
password = '123456'

#user = auth.create_user_with_email_and_password(email,password)
#print(user)

user = auth.sign_in_with_email_and_password(email,password)
print(user)

#info = auth.get_account_info(user['idToken'])
#print(info)

auth.send_email_verification(user['idToken'])

auth.send_password_reset_email(email)