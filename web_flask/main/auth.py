from flask import render_template, flash, redirect, url_for, request, make_response
from . import Main
from models.baseModel import user_id
from .form import RegisterForm, LoginForm, RequestResetForm, ResetPasswordForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user, login_required
from .. import login_manager, mail
from flask_mail import Message
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
    return render_template('login.html', title='Login', form=form)

@Main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('Main.front_page'))


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.Email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('Main.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@Main.route('/reset', methods=['GET', 'POST'])
def reset():
    if current_user.is_authenticated:
        return redirect(url_for('Main.view'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = models.storage.access(form.email.data, 'Email', user_id)
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('Main.login'))
    return render_template('forget.html', title='Reset Password', form=form)


@Main.route("/reset/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('Main.view'))
    user = user_id.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('Main.reset'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hash_password = generate_password_hash(form.password.data)
        user.Password = hash_password
        models.storage.save()
        models.storage.close()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('Main.login'))
    return render_template('reset_pass.html', title='Reset Password', form=form)
