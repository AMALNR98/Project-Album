from email.policy import default
from enum import unique
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    fname = db.Column(db.String, nullable = False)
    lname = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False, unique = True)
    dob = db.Column(db.Date, nullable = False)
    password = db.Colum(db.String, nullable = False)

    def __repr__(self) -> str:
        return f"User({self.fname} {self.lname})"

def create_db():
    db.create_all()

