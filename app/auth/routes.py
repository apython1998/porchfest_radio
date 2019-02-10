from flask import render_template, url_for, redirect, flash, request
from werkzeug.urls import url_parse
from app import db
from app.auth import bp
from app.models import User
from flask_login import login_user, current_user, logout_user
from app.auth.forms import LoginForm, RegistrationForm


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        flash('Login successful')
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).necloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Login', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        user.save(cascade=True)
        flash('Congratulations, you are now a registered user!')
        login_user(user)
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)