from wtforms import (
    BooleanField,
    StringField,
    PasswordField,
    validators,
    DateField,
    SelectField,
    FileField,
    TextAreaField,
)
from wtforms.validators import Email, Length, DataRequired, EqualTo
from flask_wtf.file import FileRequired, FileAllowed
from flask_wtf import FlaskForm


class RegistrationForm(FlaskForm):
    fname = StringField(
        [
            Length(
                min=4,
                max=25,
            ),
            DataRequired("field required"),
        ]
    )
    lname = StringField([Length(min=0, max=25), DataRequired()])
    dob = DateField([DataRequired("field is required")])
    email = StringField(
        [Length(min=6, max=120), DataRequired("feild required"), Email("invalid email")]
    )
    password = PasswordField([DataRequired(), Length(min=6, max=35)])
    confirm = PasswordField(
        "confirm", [DataRequired("field required"), EqualTo("password")]
    )


class LoginForm(FlaskForm):
    email = StringField(
        "Email Address",
        [Length(min=6, max=120), DataRequired(), Email("email invalid")],
    )
    password = PasswordField(
        "Password",
        [
            DataRequired(),
            Length(min=6, max=35),
        ],
    )


class PhotoForm(FlaskForm):
    description = TextAreaField([Length(min=2, max=100), DataRequired()])
    photo = FileField(
        validators=[
            FileRequired(),
            FileAllowed(
                ["png", "jpeg", "jpg"],
            ),
        ]
    )
    status = SelectField(choices=[("private"), ("public")])


class AlbumForm(FlaskForm):
    name = StringField("name", [Length(min=1, max=50), DataRequired()])
    description = TextAreaField("description", [Length(min=0, max=50)])
    status = SelectField("status", choices=["Private", "Public"])
