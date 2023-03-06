#!/usr/bin/python3
from api.v1.main import main_app
from flask import abort, jsonify, request
from models.Schedule import Create_Schedule as cs
from models.Reminder import Reminder
from models import storage
from datetime import datetime, timedelta
from models.baseModel import User

bot = cs()
data = bot.View()


@main_app.route('/tasks', methods=['GET', 'POST'])
def task():
    if request.method == 'GET':
        doc = storage.view()
        data = [obj.to_json() for obj in doc.values()]
        return jsonify(data), 200

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
        return jsonify(bot.View()), 201

@main_app.route('/tasks/<int:my_id>', methods=['GET', 'PUT', 'DELETE'])
def get_task(my_id):
    doc = storage.view()
    if request.method == 'GET':
        data = [obj.to_json() for obj in doc.values()
                if obj.id == my_id]
        if data is None:
            abort(404, 'ID not in list')
        return jsonify(data)

    if request.method == 'PUT':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not JSON')
        updated_dict = {}
        for key, value in req_json.items():
            if hasattr(User, key):
                setattr(doc[my_id], key, value)
                updated_dict[key] = value
        if not updated_dict:
            abort(400, "No valid keys found")
        doc[my_id].Updated_at = datetime.now()
        storage.save()
        return jsonify(updated_dict), 200

    if request.method == 'DELETE':
        obj = doc.get(my_id)
        if obj is None:
            abort(404, 'ID not in list')
        storage.delete(obj)
        del obj
        storage.save()
        return jsonify({"Success" : "data removed"}), 200



@main_app.route('/reminder', methods=['POST'])
def reminder():
    if request.method == 'POST':
        bot = Reminder()
        req_json = request.get_json()
        bot.Twilio(**req_json)
        return jsonify({"Success" : "Reminder sent"}), 200

