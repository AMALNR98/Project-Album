from flask import Blueprint, request, url_for, flash, redirect, render_template
from flask_login import LoginManager , login_user, logout_user, login_required, current_user
from datetime import date

from .database import User, db
from .forms import RegistrationForm, LoginForm 


login_manager = LoginManager()
auth_bp = Blueprint('auth', '__name__', url_prefix='/auth')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@auth_bp.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm(request.form)

    if request.method == 'POST' and form.validate():
        user = User(fname=form.fname.data, lname=form.lname.data, email=form.email.data, dob=form.dob.data, password=form.password.data)
        if db.session.query(
            User.query.filter_by(email=form.email.data).exists()
            ).scalar():
            print('user already exists')
            return render_template('register.html', error='already registered', form=form)
        else:
            db.session.add(user)
            db.session.commit()
            print('user added successfully')
            return redirect(url_for("auth.login"))
    elif request.method == 'POST' and  form.validate() is False:
        return render_template('register.html', form=form, errors='validation error')
    else:
        return render_template('register.html', form=form, )

@auth_bp.route('/login', methods=['POST', 'GET'])
def login():
    print(current_user)
    if current_user.is_authenticated:
        return("method not allowed"), 405
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            error = ('no such email')
        elif not user.check_password(form.password.data):
            error = "invalid password"
        else:
            login_user(user)
            return "login successful"

            
    return render_template('login.html', form=form, error=error)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('album.index'))

