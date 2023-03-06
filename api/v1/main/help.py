#!/usr/bin/python3
from api.v1.main import main_app
from flask import abort, jsonify, request
from models.Schedule import Create_Schedule as cs
from models import storage
from models.checker import Checker
import json
import yaml

obj = {}
quiz_answers = {}
bot = storage.view()

@main_app.route('/help', methods=['GET', 'POST'])
def help():
    message = {}
    bot = Checker()
    req_data = request.get_json()
    if request.method == 'POST':
        for text in req_data.values():
            data = bot.Help(text)
            message[text] = data
            return jsonify(message)
    else:
        abort(404, 'invalid request')


@main_app.route('/quiz', methods=['GET', 'POST'])
def quiz():
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
                Checker.check_answers(data, int(Key))
                message = {}
                message[Key] = data
                with open('tasks.yaml', 'w') as f:
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

