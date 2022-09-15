from unicodedata import name
from flask import Blueprint, render_template
from flask_login import current_user

from album.database import Album

album_bp = Blueprint('album', '__name__')

@album_bp.route('/')
def index():
    list_of_albums = current_user.albums 

    print(list_of_albums)
    print(current_user.id)
    return render_template('home.html', user=current_user, albums = list_of_albums)






