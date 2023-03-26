#!/usr/bin/python3
from flask import render_template, flash, redirect, url_for
from . import Main 
from flask_login import current_user
"""
     renders  a template for the chatbot functionality
"""
@Main.route('/help')
def help():
    ID = current_user.id
    user = current_user.User_name
    if not ID:
        flash('Please login to access this page', 'danger')
        return redirect(url_for('Main.login'))
    return render_template('help.html', user=user) 

