#!/usr/bin/python3
from flask import render_template, flash, redirect, url_for, jsonify, request
from . import Main 
from .form import  ResetPasswordForm
from flask_login import current_user, login_required
from models.baseModel import user_id
from werkzeug.security import generate_password_hash, check_password_hash
import models
import redis
import json 

redis_client = redis.Redis(host='localhost', port=6379, db=0)
"""
     renders  a template for the chatbot functionality
"""
@Main.route('/help', methods=['GET', 'POST'])
@login_required
def help():
    ID = current_user.id
    user = current_user.User_name
    history = redis_client.get('conversation_history')
    if history is None:
        history = []
    else:
        history = json.loads(history)
    if not ID:
        flash('Please login to access this page', 'danger')
        return redirect(url_for('Main.login'))
    return render_template('help.html', user=user, data=history, ID=ID) 

@Main.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    ID = current_user.id
    user = current_user.User_name
    Email = current_user.Email
    phone = current_user.Phone_number
    form = ResetPasswordForm()
    dic = {'user': user,
           'Email': Email,
           'phone': phone,
           'ID': ID
        }
    if form.validate_on_submit():
       ''' usr = models.storage.access(ID, 'id', user_id)
        if usr and check_password_hash(usr.Password, form.old_password.data):
            hash_password = generate_password_hash(form.password.data)
            user.Password = hash_password
            models.storage.save()
            models.storage.close()
            flash('Password successfully changed', 'success')
            if request.is_xhr:
                return jsonify({'message': 'Password successfully changed'})
        else:
            if request.is_xhr:
                return jsonify({'message': 'Password not changed, please try again'})
        #if not ID:
         #   flash('Please login to access this page', 'danger')
          #  return redirect(url_for('Main.login'))
    elif request.method == 'GET': '''
    return render_template('settings.html', data=dic, form=form)
