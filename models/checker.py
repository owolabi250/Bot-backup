#!/usr/bin/python3i
from models.Schedule import Create_Schedule
import os
import models
import openai
import json
import yaml
import requests
import urllib3

class Checker:
    task_ID = None
    def __init__(self):
        """
            class modifies the Average and Target column of the User
            database
        """
        self.schedule = Create_Schedule()
        self.task = self.schedule.View("daily")
        for key, value in self.task.items():
            self.task_ID = key
            text = self.task[key]['Topic']
            self.message = f"where can i best learn the following topic {text}\
                            recommend alongsides resources"
            self.question = f"test my knowledge on the following topic {text}\
                            by asking exactly 10 objective questions"

    @classmethod
# generate average score from quiz section from the response received from openai api request
    def check_answers(cls, data, Id=None):
        response_dict = data
        num_true = len(response_dict["True"])
        num_false = len(response_dict["False"])
        if num_true + num_false == 0:
            average = 0
        else:
            average = num_true / (num_true + num_false) * 100
#save average score gained to user database
        if Id:
            DB = models.storage.view()
            DB[Id].Average = average
            DB[Id].Target = 1
            models.storage.save()

        return average

    @classmethod
# make request to openai api end point to access each question received from client side
    def _invoke_chatbot(cls, data):
        openai.api_key = os.environ['OPENAI_API_KEY']
        response_dict = {"True": {}, "False": {}}
        Value = None
        for k, v in data.items():
            Value = v

        for question, answer in Value.items():
            prompt = f"Based on this Question: {question} determine if this statement is true or false? {answer}"
            response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt= prompt,
                    temperature=0.3,
                    max_tokens=150,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0
                    )
            summary = response.choices[0].text.strip()
# Quary API response to get questions that have a true value key
# Quary API response to get questions that have a true value key
            if "True" in summary:
                response_dict["True"][question] = answer

            elif "False" in summary:
                response_dict["False"][question] = answer
        with open('checked_answer.json', 'w') as file:
            json.dump(response_dict, file)
        return response_dict

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
            openai.api_key = os.environ['OPENAI_API_KEY']
            response = openai.Completion.create(
                        model="text-davinci-003",
                        prompt= opt,
                        temperature=0.3,
                        max_tokens=150,
                        top_p=1.0,
                        frequency_penalty=0.0,
                        presence_penalty=0.0
                            )
            """
                returns a JSON value of the API response
            """
            with open('response.json', 'w') as file:
                json.dump(response, file)
            answer = response.choices[0].text
            return answer.strip()
        except urllib3.exceptions.NewConnectionError:
            return f"Connection Error, please check your internet connection"


    def Question(self, **kwargs):
        if kwargs:
            opt = kwargs.get('question')
        else:
            opt = self.question
        dic = {}
        new_dic = {}
        data = self.Help(opt)
        dic["tasks"] = data
        obj = dic["tasks"].split("\n")
        for key in range(len(obj)):
            new_dic[key] = obj[key]
        new_dic = {key: value for key, value in new_dic.items() if value != ''}
        with open('tasks.yaml', 'a') as file:
            yaml.dump(new_dic, file)
        return new_dic
        
    

