#!/usr/bin/python3i
from models.Schedule import Create_Schedule
import os
import models
import openai
import json
import yaml
import logging
import redis


redis_client = redis.Redis(host='localhost', port=6379, db=0)


class Checker:
    task_ID = None

    def __init__(self, my_id, table=None):
        self.my_id = my_id
        self.table = table
        """
            class modifies the Average and Target column of the User
            database
        """
        self.schedule = Create_Schedule(self.my_id)
        if self.table:
            self.task = self.schedule.View(self.my_id, "daily", self.table)
        else:
            self.task = self.schedule.View(self.my_id, "daily")
        for key, _ in self.task.items():
            self.task_ID = key
            text = self.task[key]['Topic']
            self.message = f"""where can i best learn the following topic
                                {text}recommend alongsides resources"""
            self.question = f"""test my knowledge on the following topic {text}
                            by asking exactly 10 none objective questions"""
    """
        class method generate average score gotten from the user quiz section
        based on the response received from openai api request
    """
    @classmethod
    def check_answers(cls, data, usr, Id=None):
        try:
            response_dict = data
            num_true = len(response_dict["True"])
            num_false = len(response_dict["False"])
            if num_true + num_false == 0:
                average = 0
            else:
                average = num_true / (num_true + num_false) * 100

            if Id:
                DB = models.storage.view(usr)[0].get(usr)
                DB = DB.schedules
                for index, task in enumerate(DB):
                    if task.id == Id:
                        DB[index].Average = average
                        DB[index].Target = 1
                        models.storage.save()
            return average
        except Exception as e:
            return f"the following Error occured {e}"

    """
        class method uses the openAI API to invoke a chatbot to check and
        validate the quiz answers sent from the user quiz session
        and then return a dictionary of the true and false answers
    """
    @classmethod
    def _invoke_chatbot(cls, data):
        try:
            openai.api_key = os.environ['OPENAI_API_KEY']
            response_dict = {"True": {}, "False": {}}
            Value = None
            for _, v in data.items():
                Value = v

            for question, answer in Value.items():
                prompt = f"""Based on this question: {question}, determine
                            if the following statement is true or false:
                            {answer}? If the answer cannot be determined,
                            please respond with false."""
                response = openai.Completion.create(
                                model="text-davinci-003",
                                prompt=prompt,
                                temperature=0.3,
                                max_tokens=200,
                                top_p=1.0,
                                frequency_penalty=0.0,
                                presence_penalty=0.0)
# Quary API response to get questions that have a true  or false value key
                if response.choices and "True" in response.choices[0].text:
                    response_dict["True"][question] = answer
                elif response.choices and "False" in response.choices[0].text:
                    response_dict["False"][question] = answer
            with open('checked_answer.json', 'a') as file:
                json.dump(response_dict, file)
            return response_dict
        except Exception as e:
            logging.exception("Error invoking chatbot")
            raise e

    def Help(self, message=None):
        """
            class method uses the openAI API to invoke a chatbot to recommend
            resources based on the daily topic queried from the database
            or questions asked
        """
        try:
            if message is None:
                opt = self.message
            else:
                opt = message
            conversation_history = redis_client.get('conversation_history')
            if conversation_history is None:
                conversation_history = []
            else:
                conversation_history = json.loads(
                                            conversation_history.decode())

            conversation_history.append({"role": "user", "content": opt,
                                         "ID": self.my_id})
            messages = [
                        {"role": "system", "content": f"{opt}"}
                ]
            answer = self.Bot(messages)
            """
                returns a JSON value of the API response
            """
            with open('response.json', 'a') as file:
                json.dump(answer, file)
            conversation_history.append({"role": "bot", "content": answer,
                                        "ID": self.my_id})
            redis_client.set('conversation_history', json.dumps(
                                                    conversation_history))
            return answer.strip()
        except Exception as e:
            logging.exception("Error invoking chatbot")
            raise e

    def Question(self, **kwargs):
        try:
            if kwargs:
                opt = kwargs.get('question')
            else:
                opt = self.question
            dic = {}
            new_dic = {}
            model = "text-davinci-003"
            data = self.Bot(opt, model)
            dic["tasks"] = data
            obj = dic["tasks"].split("\n")
            for key in range(len(obj)):
                new_dic[key] = obj[key]
            new_dic = {key: value for key, value in new_dic.items()
                       if value != ''}
            with open('tasks.yaml', 'a') as file:
                yaml.dump(new_dic, file)
            return new_dic
        except Exception as e:
            logging.exception("Error invoking chatbot")
            raise e

    def Bot(self, prompt, model=None):
        openai.api_key = os.environ['OPENAI_API_KEY']
        if model is None:
            model = "gpt-3.5-turbo"
            response = openai.ChatCompletion.create(
                    model=model,
                    messages=prompt,
                    temperature=0.3,
                    max_tokens=150,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0
                    )
            answer = response['choices'][0]['message']['content'].strip()
            return answer
        else:
            response = openai.Completion.create(
                model=model,
                prompt=prompt,
                temperature=0.3,
                max_tokens=150,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
                )
            answer = response['choices'][0]['text'].strip()
            return answer
