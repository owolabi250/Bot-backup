import requests

def get_recommendations(task):

   # for task in tasks:
        # Search for topics related to the task
    response = requests.get(f'https://api.github.com/search/topics?q={task}')
    topics = response.json()
        # Add the top topic to the recommendations list
  #      if topics:
   #         top_topic = topics[0]['name']
    #        recommendations.append(top_topic)
    return topics

