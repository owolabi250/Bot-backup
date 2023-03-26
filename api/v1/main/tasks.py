#!/usr/bin/python3
from api.v1.main import main_app
from flask import abort, jsonify, request
from models.Schedule import Create_Schedule as cs
from models.Reminder import Reminder
from models import storage
from datetime import datetime, timedelta
from flask_login import current_user, login_required
from models.baseModel import User, user_id, AutoSchedule, JSCourse
from functools import wraps
import jwt
import json

#bot = cs()
#data = bot.View()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        from ..app import app
        token = None
        data = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = storage.access(data["user_id"], 'id', user_id)
        except:
            return jsonify({"message" : "Token is invalid!"}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@main_app.route('/tasks', methods=['GET', 'POST'])
@token_required
def task(current_user):
    ID = current_user.id
    bot = cs(ID)
    if request.method == 'GET':
        doc = storage.view(ID)[1]
        return jsonify(doc), 200

    if request.method == 'POST':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        if req_json.get("Day") is None:
            abort(400, 'Missing Date')
        if req_json.get("Course") is None:
            abort(400, 'Missing Course')
        if req_json.get("Topic") is None:
            abort(400, 'Missing Topic')
        if req_json.get("Reminder") is None:
            abort(400, 'please set reminder')
        bot.Create(**req_json)
        bot.Save()
        return jsonify(bot.View(ID)), 201

@main_app.route('/tasks/<int:my_id>', methods=['GET', 'PUT', 'DELETE'])
@token_required
def get_task(current_user, my_id):
    ID = current_user.id
    data = storage.view(ID)[0].get(ID)
    file = storage.view(ID)[1]
    doc = data.schedules
    if request.method == 'GET':
        for key, value in file.items():
            if key == my_id:
                data = value
                return jsonify(data), 200
            elif key != my_id:
                return jsonify({"message" : "ID not in list"}), 404

    if request.method == 'PUT':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not JSON')
        updated_dict = {}
        for key, value in req_json.items():
            for index, task in enumerate(doc):
                if task.id == my_id:
                    if hasattr(task, key):
                        setattr(doc[index], key, value)
                    updated_dict[key] = value
                    doc[index].Updated_at = datetime.now()
        if not updated_dict:
            abort(400, "No valid keys found")
        storage.save()
        return jsonify(updated_dict), 200

    if request.method == 'DELETE':
        obj = None
        for item in doc:
            if item.id == my_id:
                obj = item
        if obj is None:
            abort(404, 'ID not in list')
        storage.delete(obj)
        del obj
        storage.save()
        return jsonify({"Success" : "data removed"}), 200



@main_app.route('/reminder', methods=['POST'])
@token_required
def reminder(current_user):
    ID = current_user.id
    if request.method == 'POST':
        bot = Reminder(ID)
        req_json = request.get_json()
        bot.Twilio(**req_json)
        return jsonify({"Success" : "Reminder sent"}), 200

@main_app.route('/auto-dash', methods=['POST'])
@token_required
def auto_dash(current_user):
    ID = current_user.id
    data = storage.view(ID)[0].get(ID)
    files = {
            "Python" : [AutoSchedule, data.auto_schedules, 'Python_Courses.json'],
            "Javascript" : [JSCourse, data.JScourse, 'JSCourse.json']
            }
    req_json = request.get_json()
    course = req_json.get('Course')
    doc = None
    key = None
    if course in files:
        doc = files.get(course)
    if doc:
        key = [i for i in doc[1] if i.user_ID == ID]
    now = datetime.utcnow().date()

    if request.method == 'POST':
        day = req_json.get("Day")
        day = datetime.strptime(day, "%Y-%m-%d").date()
 
         # Check if the specified date is in the past
        if day < now:
            return jsonify({"message": "Date is in the past"}), 400
 
 # Check if the user already has a task set for this day
        if key:
            return jsonify({"message": "User task already set"}), 400
 
         # Create a new schedule for the user
        if doc: 
            with open(doc[2], 'r') as f:
                courses = json.load(f)
                file = [v for v in courses.values()]
                for i, topic in enumerate(file):
                    date = day + timedelta(days=i)
                    task = doc[0](user_ID=ID,
                                    Days=date,
                                    Course=topic["Course"],
                                    Topic=topic["Topic"],
                                    Reminder=req_json.get("Reminder"),
                                    Created_at=now)
                    storage.new(task)
            storage.save()
            return jsonify({"Success": "Auto dash set"}), 200
        else:
            return jsonify({"message": "Course not found"}), 400
 


