from flask import Blueprint

album_bp = Blueprint('album', '__name__')

@album_bp.route('/')
def index():
    return 'index page'



