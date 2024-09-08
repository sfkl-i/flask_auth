from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint
from flask_project.forms.login import LoginForm
from flask_project.forms.singup import SignupForm
from flask_project.models.user import User
from flask_project.models.base import Session

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.protected'))

    form = LoginForm()
    if form.validate_on_submit():
        with Session() as session:
            user = session.query(User).filter_by(nickname=form.nickname.data).first()
            if user and check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('auth.protected'))
            else:
                flash('Invalid nickname or password.')
    return render_template('login.html', form=form)


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        with Session() as session:
            user = session.query(User).filter_by(email=form.email.data).first()
            if user:
                flash('Email already registered.')
                return redirect(url_for('auth.signup'))

            hashed_password = generate_password_hash(form.password.data)
            new_user = User(
                nickname=form.nickname.data,
                email=form.email.data,
                password=hashed_password
            )
            session.add(new_user)
            session.commit()
            login_user(new_user)
            return redirect(url_for('auth.protected'))

    return render_template('signup.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth_bp.route('/protected')
@login_required
def protected():
    return render_template('protected.html', name=current_user.nickname)
