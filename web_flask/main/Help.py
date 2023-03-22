#!/usr/bin/python3
from flask import render_template, flash, redirect, url_for
from . import Main 
from flask_login import current_user
"""
     renders  a template for the chatbot functionality
"""
@Main.route('/help')
def help():
    user = current_user.User_name
    return render_template('help.html', user=user) 

