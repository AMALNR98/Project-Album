from flask import Blueprint, render_template
from flask_login import current_user

album_bp = Blueprint('album', '__name__')

@album_bp.route('/')
def index():
    return render_template('home.html', user=current_user)




