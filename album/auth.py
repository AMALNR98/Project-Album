from flask import Blueprint

auth_bp = Blueprint('auth', '__name__', url_prefix='/auth')


@auth_bp.route('/register')
def register():
    return "registration page"


@auth_bp.route('/register')
def login():
    return "registration page"

