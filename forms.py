from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators,BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[validators.Length(min=2, max=20), validators.DataRequired()])
    email = StringField('Email', validators=[validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[validators.DataRequired(), validators.EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired(), Length(min=8, message='Password must be at least 8 characters long')])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Reset Password')
