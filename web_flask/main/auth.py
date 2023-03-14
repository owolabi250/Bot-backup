from flask import render_template, flash, redirect, url_for, request, make_response
from . import Main
from models.baseModel import user_id
from .form import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user, login_required
from .. import login_manager
import models
import uuid
import datetime
import jwt


@login_manager.user_loader
def load_user(User_id):
    return models.storage.access(User_id, 'id', user_id)


@Main.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        password = generate_password_hash(form.password.data)
        user = user_id(id=str(uuid.uuid4()), User_name=form.username.data,
                       Email=form.email.data, Password=password)
        models.storage.new(user)
        models.storage.save()
        models.storage.close()
        flash(f'Account created successfully for {form.username.data}', 'success')

        return redirect(url_for('Main.login'))
    return render_template('register.html', form=form)

@Main.route("/login", methods=['GET', 'POST'])
def login():
    from ..app import app
    if current_user.is_authenticated:
        return redirect(url_for('Main.view'))
    form = LoginForm()
    if form.validate_on_submit():
        user = models.storage.access(form.email.data, 'Email', user_id)
        if user and check_password_hash(user.Password, form.password.data):
            login_user(user, remember=form.remember.data)
            my_id = current_user.id
            token = jwt.encode({'user_id': my_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, app.config['SECRET_KEY'])
            flash(f'You are logged in!', 'success')
            next_page = request.args.get('next')
            response = redirect(next_page) if next_page else redirect(url_for('Main.view'))
            tok = token.encode('UTF-8').decode()
            response.set_cookie('access_token', tok)
            return response
        else:
            flash(f'Login Unsuccessful. Please check username and password', 'danger')
            return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
    return render_template('login.html', title='Login', form=form)

@Main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('Main.front_page'))

