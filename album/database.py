from sqlalchemy import func
from sqlalchemy.ext.hybrid import hybrid_property
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash 


db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    fname = db.Column(db.String, nullable = False)
    lname = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False, unique = True)
    dob = db.Column(db.String, nullable = False)
    _password = db.Column(db.String, nullable = False)
    albums = db.relationship("Album", lazy ="dynamic")
    bio = db.Column(db.String, nullable = True)
    


    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        """Store the password as a hash for security."""
        self._password = generate_password_hash(value)

    def check_password(self, value):
        return check_password_hash(self._password, value)

    def __repr__(self) -> str:
        return f"User({self.fname} {self.lname})"


class Album(db.Model):
    __tablename__ = "albums"
    id = db.Column(db.Integer, primary_key =True)
    name = db.Column(db.String, nullable = False)
    description = db.Column(db.String)
    create_date = db.Column(db.String, default = func.now(), nullable = False)
    last_opened = db.Column(db.String, onupdate = func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    public = db.Column(db.Boolean, default=False, nullable=False)
    photos = db.relationship("Photo", lazy='dynamic', cascade="all,delete")
    __table_args__ = (db.UniqueConstraint('user_id', 'name', name='_user_id_name_uc'),)
    def __repr__(self) -> str:
        return f"Album({self.name})"



class Photo(db.Model):
    __tablename__ = "photos"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Integer, nullable = False)
    size = db.Column(db.Integer, nullable = False)
    description = db.Column(db.String)
    last_opened = db.Column(db.String, onupdate = func.now())
    uploaded_date = db.Column(db.String, default = func.now(), nullable = False)
    album_id = db.Column(db.Integer, db.ForeignKey("albums.id"), nullable = False)       
    public = db.Column(db.Boolean, default=False, nullable=False)
    likes = db.Column(db.Integer, default=0)
    comments = db.relationship("Comment", lazy='dynamic')
    __table_args__ = (db.UniqueConstraint('album_id', 'name', name='_album_id_name_uc'),)

    def __repr__(self) -> str:
        return f"Photo({self.name})"


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key = True)
    display_name = db.Column(db.Integer, nullable = False)
    created_date = db.Column(db.String, default = func.now(), nullable = False)
    photo_id = db.Column(db.Integer, db.ForeignKey("photos.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    comment = db.Column(db.String, nullable = False)

    def __repr__(self) -> str:
        return f"Comment({self.name})"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
 


