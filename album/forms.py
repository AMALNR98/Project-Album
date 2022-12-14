from wtforms import (
    BooleanField,
    StringField,
    PasswordField,
    DateField,
    SelectField,
    FileField,
    TextAreaField,
)
from wtforms.validators import Email, Length, DataRequired, EqualTo
from flask_wtf.file import FileRequired, FileAllowed
from flask_wtf import FlaskForm, Form


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
    status = SelectField(choices=[("private",), ("public",)])


class AlbumForm(FlaskForm):
    name = StringField("name", [Length(min=1, max=50), DataRequired()])
    description = TextAreaField("description", [Length(min=0, max=50)])
    status = SelectField("status", choices=["Private", "Public"])


class CommentForm(FlaskForm):
    display_name = StringField("name", [Length(min=1, max=50), DataRequired()])
    comment = TextAreaField("description", [Length(min=0, max=50)])


class ProfileForm(Form):
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
    bio = TextAreaField([Length(min=0, max=100)])
    public = BooleanField("make user searchable")
    photo = FileField(
        validators=[
            FileAllowed(
                ["png", "jpeg", "jpg"],
            ),
        ]
    )
    email = StringField(
        [Length(min=6, max=120), DataRequired("field required"), Email("invalid email")]
    )
