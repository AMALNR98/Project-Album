from sqlite3 import Date
from tkinter.tix import Form
from wtforms import  Form, BooleanField, StringField, PasswordField, validators, DateField

class RegistrationForm(Form):
    fname = StringField('First Name', [validators.Length(min=4, max=25)])
    lname = StringField('Last Name', [validators.Length(min=4, max=25)])
    dob = DateField('date of birth')
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
