from flask import Flask, render_template, abort, url_for
from models.Schedule import Create_Schedule
from models.checker import Checker
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_mail import Mail
from . import Main
from .. import db
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


@Main.route('/missed')
def missed():
    bot = Create_Schedule()
    dic = bot.View('missed')
    return render_template('task_status.html', data=dic)

@Main.route('/daily')
def daily():
    bot = Create_Schedule()
    dic = bot.View('daily')
    return render_template('task_status.html', data=dic)

@Main.route('/View')
def view():
    bot = Create_Schedule()
    doc = bot.View()
    return render_template('index.html', data=doc)

@Main.route('/upcoming')
def upcoming():
    bot = Create_Schedule()
    dic = bot.View('upcoming')
    return render_template('task_status.html', data=dic)

@Main.route('/new')
def new():
    return render_template('table.html')

@Main.route('/quiz')
def quiz():
    global quiz_data # declare global variable
    
    bot = Checker()
    data_id = bot.task_ID
    if not bot.task or not data_id:
        return f"Sorry, there are no tasks available at the moment."
    if not quiz_data: # check if global variable is not empty
        dic = bot.Question()
        quiz_data = dic # store results in global variable
        return render_template('quiz.html', data=dic, data_ID=data_id)
    else:
        return render_template('quiz.html', data=quiz_data, data_ID=data_id)

