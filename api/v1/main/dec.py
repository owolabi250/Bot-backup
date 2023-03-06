import json

def tick():
    with open('checked-answers.json', 'r') as f:
        data = json.load(f)
    return data
