from flask import Flask, render_template, abort, url_for, redirect, flash, request
from models.Schedule import Create_Schedule
from models.checker import Checker
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_mail import Mail
from flask_login import login_required, current_user
from . import Main
import os
import models
import json


"""
    This file contains all the routes for the application
    this enables user to query the database to view Schedules
    based on the status of the task
"""
quiz_data = {}
auto = False
course = None

@Main.route('/')
def front_page():
    return render_template('landing_page.html')


@Main.route('/about')
def about():
    return render_template('about.html')


@Main.route('/missed',  methods=['GET'])
@login_required
def missed():
    my_id = current_user.id
    user = current_user.User_name
    if not my_id:
        flash('You need to be logged in to view this page', 'danger')
        return redirect(url_for('Main.login'))
    bot = Create_Schedule(my_id)
    if auto:
        dic = bot.View(my_id, 'missed', course)
        return render_template('task_status.html', data=dic, state=auto, user=user)
    else:
        dic = bot.View(my_id, 'missed')
        return render_template('task_status.html', data=dic, user=user)

@Main.route('/daily', methods=['GET'])
@login_required
def daily():
    my_id = current_user.id
    user = current_user.User_name
    if not my_id:
        flash('You need to be logged in to view this page', 'danger')
        return redirect(url_for('Main.login'))
    bot = Create_Schedule(my_id)
    if auto:
        dic = bot.View(my_id, 'daily', course)
        return render_template('task_status.html', data=dic, state=auto, user=user)
    else:
        dic = bot.View(my_id, 'daily')
        return render_template('task_status.html', data=dic, user=user)

@Main.route('/View', methods=['GET'])
@login_required
def view():
    global auto
    my_id = current_user.id
    user = current_user.User_name
    if not my_id:
        flash('You need to be logged in to view this page', 'danger')
        return redirect(url_for('Main.login'))
    bot = Create_Schedule(my_id)
    dic = bot.View(my_id)
    auto = False
    return render_template('index.html', data=dic, status=auto, user=user)

@Main.route('/upcoming')
@login_required
def upcoming():
    my_id = current_user.id
    user = current_user.User_name
    if not my_id:
        flash('You need to be logged in to view this page', 'danger')
        return redirect(url_for('Main.login'))
    bot = Create_Schedule(my_id)
    if auto:
        dic = bot.View(my_id, 'upcoming', course)
        return render_template('task_status.html', data=dic, state=auto, user=user)
    else:
        dic = bot.View(my_id, 'upcoming')
        return render_template('task_status.html', data=dic, user=user)

@Main.route('/new')
@login_required
def new():
    return render_template('table.html')

@Main.route('/quiz')
@login_required
def quiz():
    global quiz_data # declare global variable
    ID = current_user.id
    user = current_user.User_name
    if not ID:
        flash('You need to be logged in to view this page', 'danger')
        return redirect(url_for('Main.login'))
    if auto:
        bot = Checker(ID, course)
        data_id = bot.task_ID
    else:
        bot = Checker(ID)
        data_id = bot.task_ID
    if not bot.task or not data_id:
        return f"Sorry, there are no tasks available at the moment."
    if not quiz_data: # check if global variable is not empty
        dic = bot.Question()
        quiz_data = dic # store results in global variable
        return render_template('quiz.html', data=dic, data_ID=data_id, user=user)
    else:
        return render_template('quiz.html', data=quiz_data, data_ID=data_id, user=user)

@Main.route('/auto_dash', methods=['GET'])
@login_required
def dashboard():
    global auto, course
    ID = current_user.id
    user = current_user.User_name
    if not ID:
        flash('You need to be logged in to view this page', 'danger')
        return redirect(url_for('Main.login'))
    data = models.storage.view(ID)[0].get(ID)
    files = {
            "Python" : data.auto_schedules,
            "Javascript" : data.JScourse,
            "React" : data.Reactcourse,
            "C" : data.C_course
        }
    course = request.args.get('myID')
    doc = None
    key = None
    if course in files:
        doc = files.get(course)
    if doc:
        key = [i for i in doc if i.user_ID == ID]
    if key:
        auto = True
        return render_template('auto_dash.html', data=doc, status=auto, user=user)
    else:
        return render_template('auto_reg.html')


@Main.route('/articles', methods=['GET', 'POST'])
@login_required
def articles():
    ID = current_user.id
    if not ID:
        flash('You need to be logged in to view this page', 'danger')
        return redirect(url_for('Main.login'))
    if auto and course == 'Python':
        return render_template('articles.html', status=auto)
    elif auto and course == 'Javascript':
        return render_template('JSarticles.html', status=auto)
    elif auto and course == 'React':
        return render_template('Reactarticles.html', status=auto)
    elif auto and course == 'C':
        return render_template('C_articles.html', status=auto)
    else:
        return render_template('auto_reg.html')
