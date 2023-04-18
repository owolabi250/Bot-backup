#!/usr/bin/python3
from api.v1.main import main_app
from flask import abort, jsonify, request
from models.Schedule import Create_Schedule as cs
from models import storage
from models.checker import Checker
from models.baseModel import user_id
from .tasks import token_required
from werkzeug.security import check_password_hash, generate_password_hash
from .res import get_recommendations, get_resource
from flask_mail import Message
from .netT import send_email
from datetime import datetime, timedelta
import json
import yaml
import redis

obj = {}
quiz_answers = {}
redis_client = redis.Redis(host='localhost', port=6379, db=0)
"""
def send_reset_email(user):
      try:
          token = user.generate_confirmation_code()
          code = token[0]
          msg = Message('Confirmation token',
                          sender='noreply@demo.com',
                          recipients=[user.Email])
          msg.body = f'Your confirmation code is: {code}'
          result = mail.send(msg)
          if result is not None:
              return True
          else:
              return False
      except Exception as e:
          return f'{e}'
"""

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
    if request.method == 'DELETE':
        history = redis_client.get('conversation_history')
        if history is None:
            history = []
        else:
            history = json.loads(history.decode('utf-8'))
            newData = [item for item in history if item['ID'] != ID]
            redis_client.set('conversation_history', json.dumps(newData))
        return jsonify({"message": "successfully removed"}), 200
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
    new_key = ''.join(new_key).split('.')
    new_key.pop(0)
    if request.method == 'POST':
        if quiz_answers is None:
            abort(404, 'invalid request')
        else:
            if not obj:
                for _, values in Value.items():
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

@main_app.route('/articles', methods=['GET', 'POST'])
@token_required
def articles(current_user):
    if request.method == 'POST':
        task = request.json.get('task')
        if task is None:
            abort(404, 'invalid request')
        else:
            file = {}
            data = get_recommendations(task)
            if data is None:
                abort(404, 'invalid request')
            else:
                source = get_resource(data)
                file[task] = source
                with open('Python_resources.json', 'w') as f:
                    json.dump(file, f)
                filtered_list = list(filter(lambda x: x.strip(), source))
                return jsonify(filtered_list), 200

@main_app.route('/settings/', methods=['POST', 'PUT', 'DELETE'])
@token_required
def settings(current_user):
    ID = current_user.id
    data = request.get_json()
    usr = storage.access(ID, 'id', user_id)
    course_list = cs(ID)
    if request.method == 'PUT':
        if data is None:
            abort(404, 'invalid credentials')
        else:
            if data.get('option') == 'username':
                obj = data.get('Key')
                if obj is not None:
                    if usr and check_password_hash(usr.Password, obj):
                        usr.User_name = data.get('Value')
                        usr.Updated_at = datetime.now().strftime("%Y-%m-%d")
                        storage.save()
                        storage.close()
                        return jsonify({"message": "successfully updated"}), 200
                    else:
                        abort(404, 'invalid credentials')
            elif data.get('option') == 'emailreset':
                email = data.get('email')
                key = data.get('passkey')
               # if not validation.is_valid(email):
                 #   abort(404, 'invalid email')
                if usr and check_password_hash(usr.Password, key):
                    usr.Email = email
                    usr.Updated_at = datetime.now().strftime("%Y-%m-%d")
                    storage.save()
                    storage.close()
                    return jsonify({"message": "successfully updated"}), 200
                else:
                    abort(404, 'invalid credentials')
            elif data.get('option') == 'course_tempo':
                course = data.get('course')
                course_file = course_list.Target(ID, course)[1]
                delta = 0
                if course_file:
                    tempo = data.get('tempo')
                    course_file = course_file.get(course)
                    now = datetime.utcnow().date()
                    for item in course_file:
                        cur_date = datetime.strptime(item.Days, '%Y-%m-%d').date()
                        #cur_date = cur_date + timedelta(days=tempo)
                        if cur_date >= now:
                            delta = delta + tempo
                            cur_date = cur_date + timedelta(days=delta)
                            item.Days = cur_date.strftime('%Y-%m-%d')
                    storage.save()
                    storage.close()
                    return jsonify({"message": "successfully updated"}), 200
                else:
                    abort(404, 'Not registered for course')

            elif data.get('option') == 'contact':
                usr.Phone_number = data.get('phone_number')
                usr.Updated_at = datetime.now().strftime("%Y-%m-%d")
                storage.save()
                storage.close()
                return jsonify({"message": "successfully updated"}), 200

            elif data.get('option') == 'password':
                obj = data.get('old_password')
                if obj is not None:
                    if usr and check_password_hash(usr.Password, obj):
                        if data.get('new_password') == data.get('confirm_password'):
                            usr.Password = generate_password_hash(data.get('new_password'))
                            usr.Updated_at = datetime.now().strftime("%Y-%m-%d")
                            storage.save()
                            storage.close()
                            return jsonify({"message": "successfully updated",
                                            "status": 'success'}), 200
                        else:
                            return jsonify({"message": "passwords do not match",
                                            "status": 'failed'})
                    else:
                        return jsonify({"message": "invalid credentials"})
            else:
                abort(404, 'invalid request')
    if request.method == 'POST':
        if data.get('option') == 'email':
            if usr:
                send_email(usr)
                return jsonify({"message": "confirmation mail sent"}), 200
            else:
                abort(404, 'invalid credentials')
        elif data.get('option') == 'confirmation'.lower():
            code = data.get('code')
            if usr.verify_confirmation_code(code):
                return jsonify({"message": "code valid"}), 200
            else:
                abort(404, 'invalid code')
        
        elif data.get('option') == 'checkBox':
            opt = data.get('isChecked')
            usr.save_history = opt
            storage.save()
            storage.close()
            return jsonify({"message": "success"}), 200

    if request.method == 'DELETE':
        ID = current_user.id
        if data.get('option') == 'chatHistory':
            if ID != data.get('id'):
                abort(404, 'invalid credentials')
            else:
                history = redis_client.get('conversation_history')
                if history is None:
                    return jsonify({"message": "no history"}), 200
                chat_history = json.loads(history.decode('utf-8'))
                chat_history = list(filter(lambda x: x['ID'] != ID, chat_history))
                redis_client.set('conversation_history', json.dumps(chat_history))
                return jsonify({"message": "successfully deleted"}), 200
        elif data.get('option') == 'deleteCourse':
            key = data.get('course')
            course = course_list.Target(ID, key)[1]
            file = None
            course_file = course.get(key)
            if course_file:
                for item in course_file:
                    if item.user_ID == ID:
                        file = item
                    storage.delete(file)
                    storage.save()
                storage.close()
                return jsonify({"message": f"deleted {key} tutorial successfully"}), 200
            abort(404, 'record not found')

        elif data.get('option') == 'deleteAccount':
            confirmDelete = data.get('confirmDelete')
            user = storage.view(ID)[0].get(ID)
            Auto_courses = ["Python", "C", "React", "Javascript"]
            Delete_auto_courses = course_list.DeleteAll(ID, Auto_courses)
            Delete_custom_courses = course_list.Delete(ID, None)
            if Delete_auto_courses and Delete_custom_courses:
                if user.id == ID and confirmDelete:
                    storage.delete(user)
                    storage.save()
                storage.close()
                return jsonify({"message": "Account deleted"}), 200
        
            abort(404, 'invalid request')
    else:
        abort(404, 'invalid request')
