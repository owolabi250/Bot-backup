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



"""
    This file contains all the routes for the application
    this enables user to query the database to view Schedules
    based on the status of the task
"""
quiz_data = {}

@Main.route('/')
def front_page():
    return render_template('landing_page.html')


@Main.route('/reset')
def reset():
    return render_template('forget.html')


@Main.route('/about')
def about():
    return render_template('about.html')


@Main.route('/missed',  methods=['GET'])
@login_required
def missed():
    my_id = current_user.id
    if not my_id:
        flash('You need to be logged in to view this page', 'danger')
        return redirect(url_for('Main.login'))
    bot = Create_Schedule(my_id)
    dic = bot.View(my_id, 'missed')
    return render_template('task_status.html', data=dic)

@Main.route('/daily', methods=['GET'])
@login_required
def daily():
    my_id = current_user.id
    if not my_id:
        flash('You need to be logged in to view this page', 'danger')
        return redirect(url_for('Main.login'))
    bot = Create_Schedule(my_id)
    dic = bot.View(my_id, 'daily')
    return render_template('task_status.html', data=dic)

@Main.route('/View', methods=['GET'])
@login_required
def view():
    my_id = current_user.id
    if not my_id:
        flash('You need to be logged in to view this page', 'danger')
        return redirect(url_for('Main.login'))
    bot = Create_Schedule(my_id)
    dic = bot.View(my_id)
    return render_template('index.html', data=dic)

@Main.route('/upcoming')
@login_required
def upcoming():
    my_id = current_user.id
    if not my_id:
        flash('You need to be logged in to view this page', 'danger')
        return redirect(url_for('Main.login'))
    bot = Create_Schedule(my_id)
    dic = bot.View(my_id, 'upcoming')
    return render_template('task_status.html', data=dic)

@Main.route('/new')
@login_required
def new():
    return render_template('table.html')

@Main.route('/quiz')
@login_required
def quiz():
    global quiz_data # declare global variable
    
    ID = current_user.id
    bot = Checker(ID)
    data_id = bot.task_ID
    if not bot.task or not data_id:
        return f"Sorry, there are no tasks available at the moment."
    if not quiz_data: # check if global variable is not empty
        dic = bot.Question()
        quiz_data = dic # store results in global variable
        return render_template('quiz.html', data=dic, data_ID=data_id)
    else:
        return render_template('quiz.html', data=quiz_data, data_ID=data_id)

