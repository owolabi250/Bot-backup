from flask import render_template, flash, redirect, url_for
from . import Main
from models.baseModel import user_id
from .form import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
import models

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
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'oadava@gmail.com' and form.password.data == 'password':
            flash(f'You have been logged in!', 'success')
            return redirect(url_for('Main.view'))
        else:
            flash(f'Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)
