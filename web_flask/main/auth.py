from flask import render_template, flash, redirect, url_for
from . import Main
from .form import RegisterForm, LoginForm 

@Main.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        flash(f'Account created successfully for {form.username.data}', 'success')
        return redirect(url_for('Main.view'))
    return render_template('register.html', form=form)

@Main.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'oadava@gmail.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('Main.view'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html',  form=form)
