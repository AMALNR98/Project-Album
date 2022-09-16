from sqlite3 import Date
from wtforms import  Form,  BooleanField, StringField, PasswordField, validators, DateField, SelectField, FileField
from wtforms.validators import Email, Length, DataRequired, EqualTo
from  flask_wtf.file import FileRequired, FileAllowed
 

class RegistrationForm(Form):
    fname = StringField( [Length(min=4, max=25,), DataRequired()])
    lname = StringField( [Length(min=0, max=25), DataRequired()])
    dob = DateField( [DataRequired()])
    email = StringField( [Length(min=6, max=120), DataRequired(), Email()])
    password = PasswordField( [
        DataRequired(),
        EqualTo('confirm', message='Passwords must match'),
        Length(min=6, max=35)
    ])
    confirm = PasswordField( [DataRequired()])


class LoginForm(Form):
    email = StringField('Email Address', [Length(min=6, max=120), DataRequired(), Email()])
    password = PasswordField('New Password', [
        DataRequired(),
        Length(min=6, max=35),])


class AlbumForm(Form):
    name = StringField('name', [Length(min=1, max=50), DataRequired()])
    description = StringField('description', [Length(min=0, max=50 )])
    status = SelectField('status', choices=['Private', 'Public'])

