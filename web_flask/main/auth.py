from flask import render_template, flash, redirect, url_for, request
from . import Main
from models.baseModel import user_id
from .form import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
import models
from flask_login import login_user, current_user
from .. import login_manager


@login_manager.user_loader
def load_user(User_id):
    return models.storage.access(User_id, 'id', user_id)


@Main.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        password = generate_password_hash(form.password.data)
        user = user_id(User_name=form.username.data, Email=form.email.data, Password=password)
        models.storage.new(user)
        models.storage.save()
        models.storage.close()
        flash(f'Account created successfully for {form.username.data}', 'success')

        return redirect(url_for('Main.login'))
    return render_template('register.html', form=form)

@Main.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('Main.view'))
    form = LoginForm()
    if form.validate_on_submit():
        user = models.storage.access(form.email.data, 'Email', user_id)
        if user and check_password_hash(user.Password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'You are logged in!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('Main.view'))
        else:
            flash(f'Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)
