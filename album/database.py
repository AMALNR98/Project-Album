from sqlalchemy import func
from album import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    fname = db.Column(db.String, nullable = False)
    lname = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False, unique = True)
    dob = db.Column(db.Date, nullable = False)
    password = db.Column(db.String, nullable = False)
    albums = db.relationship("Album")


    def __repr__(self) -> str:
        return f"User({self.fname} {self.lname})"


class Album(db.Model):
    __tablename__ = "albums"
    id = db.Column(db.Integer, primary_key =True)
    name = db.Column(db.String, nullable = False)
    create_date = db.Column(db.DateTime, default = func.now(), nullable = False)
    last_opened = db.Column(db.DateTime, onupdate = func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    photos = db.relationship("Photo")
    __table_args__ = (db.UniqueConstraint('user_id', 'name', name='_user_id_name_uc'),)

    def __repr__(self) -> str:
        return f"Album({self.name})"



class Photo(db.Model):
    __tablename__ = "photos"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Integer, nullable = False)
    size = db.Column(db.Integer, nullable = False)
    last_opened = db.Column(db.DateTime, onupdate = func.now())
    uploaded_date = db.Column(db.DateTime, default = func.now(), nullable = False)
    album_id = db.Column(db.Integer, db.ForeignKey("albums.id"), nullable = False)       
    photos = db.relationship("Comment")
    __table_args__ = (db.UniqueConstraint('album_id', 'name', name='_album_id_name_uc'),)

    def __repr__(self) -> str:
        return f"Photo({self.name})"


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key = True)
    display_name = db.Column(db.Integer, nullable = False)
    photo_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, primary_key = True)
    comment = db.Column(db.String, nullable = False)

    def __repr__(self) -> str:
        return f"Comment({self.name})"


