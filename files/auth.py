from flask import Blueprint, render_template, request, flash, redirect, url_for
import re
from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if len(email) and len(password) > 0:
            user = User.query.filter_by(email=email).first()
            if user:
                if check_password_hash(user.password, password):
                    flash('Logged in successfully!', category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('views.home'))
                else:
                    flash('Password is Incorrect', category='error')
            else:
                flash('User does not Exists!', category='error')
        else:
            redirect(url_for('auth.login'))

    return render_template("login.html", text='წარმატებით შეხვედით', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        firstname = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if password1 != password2:
            flash('incorrect password.', category='error')
        elif not re.fullmatch(regex, email):
            flash('Email Format is not correct!', category='error')
        elif len(email) or len(password1) or len(firstname) == 0:
            return redirect(url_for('auth.signup'))
        else:
            user = User.query.filter_by(email=email).first()
            if user is None:
                new_user = User(email=email, password=generate_password_hash(password1, method='sha256'),
                                first_name=firstname)
                db.session.add(new_user)
                db.session.commit()
                flash("Account created", category="success")
                login_user(new_user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('account already exists', category='error')

    return render_template('sign_up.html', user=current_user)
