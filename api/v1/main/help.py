#!/usr/bin/python3
from api.v1.main import main_app
from flask import abort, jsonify, request
from models.Schedule import Create_Schedule as cs
from models import storage
from models.checker import Checker
from .tasks import token_required
import json
import yaml

obj = {}
quiz_answers = {}


@main_app.route('/help', methods=['GET', 'POST'])
@token_required
def help(current_user):
    ID = current_user.id
    message = {}
    bot = Checker(ID)
    req_data = request.get_json()
    if request.method == 'POST':
        for text in req_data.values():
            data = bot.Help(text)
            message[text] = data
            return jsonify(message), 200
    else:
        abort(404, 'invalid request')


@main_app.route('/quiz', methods=['GET', 'POST'])
@token_required
def quiz(current_user):
    ID = current_user.id
    quiz_answers = request.get_json()
    Key = None
    Value = {}
    for k, v in quiz_answers.items():
        Key = k
        Value = v
    if Key is None:
        abort(404, 'invalid request')
    
    new_key = list(Value.keys())
    new_key = ''.join(new_key)
    new_key = new_key.split('.')
    new_key.pop(0)
    if request.method == 'POST':
        if quiz_answers is None:
            abort(404, 'invalid request')
        else:
            if not obj:
                for key, values in Value.items():
                    obj[Key] = dict(zip(new_key, values))
                data = Checker._invoke_chatbot(obj)
                Checker.check_answers(data, ID, int(Key))
                message = {}
                message[Key] = data
                with open('tasks.yaml', 'a') as f:
                    yaml.dump(message, f)
                return jsonify(message), 200
            else:
                return jsonify({"message": "Quiz data already present"}), 400
    if request.method == 'GET':
        with open('tasks.yaml', 'r') as f:
            file = yaml.safe_load(f)
        if file is None:
            abort(404, 'invalid request')
        else:
            return jsonify(file), 200
