from email.policy import default
from enum import unique
from flask_sqlalchemy import SQLAlchemy, func

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


class Albums(db.Model):
    __tablename__ = "albums"
    id = db.Column(db.Integer, primary_key =True)
    name = db.Column(db.String, nullable = False)
    create_date = db.Column(db.DateTime, default = func.now(), nullable = False)
    last_opened = db.Column(db.DateTime, onupdate = func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    __table_args__ = (db.UniqueConstraint('user_id', 'name', name='_user_id_name_uc'),)
    
    def __repr__(self) -> str:
        return f"Albums({self.name})"


def create_db():
    db.create_all()