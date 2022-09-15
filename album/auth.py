from flask import Blueprint
# from wtforms import  From, BooleanField, StringField, PasswordField, validators
from .forms import RegistrationForm
from flask import request, url_for, render_template, redirect, flash

auth_bp = Blueprint('auth', '__name__', url_prefix='/auth')


# @auth_bp.route('/register')
# def register():
#     return "registration page"


@auth_bp.route('/login')
def login():
    
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        
        flash('Thanks for registering')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)
