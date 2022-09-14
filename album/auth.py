from flask import Blueprint, request, url_for, flash, redirect, render_template
from datetime import date

from .database import User, db
from .forms import RegistrationForm, LoginForm 

auth_bp = Blueprint('auth', '__name__', url_prefix='/auth')


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
    else:
        return render_template('register.html', form=form)

@auth_bp.route('/login')
def login():
    form = LoginForm(request.form)
    return render_template('login.html', form=form)


