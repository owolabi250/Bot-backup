import requests
import re
from bs4 import BeautifulSoup

def get_recommendations(task):
    url = "https://docs.python.org/3/tutorial/index.html"
    response = requests.get(url)
    search_word = task
    pattern = re.compile(search_word, re.IGNORECASE)
    soup = BeautifulSoup(response.content, 'html.parser')
    topics = []
    for item in soup.find_all('a', class_='reference internal'):
        if pattern.search(item.text):
            topics.append({'topic': item.text, 'link': item['href']})
            
    # for task in tasks:
        # Search for topics related to the task
   # response = requests.get(f'https://api.github.com/search/topics?q={task}')
   # topics = response.json()
        # Add the top topic to the recommendations list
  #      if topics:
   #         top_topic = topics[0]['name']
    #        recommendations.append(top_topic)
    return topics

def get_resource(topic):
    task = topic[0]
    task = task.get('link')
    url = f"https://docs.python.org/3/tutorial/{task}"
    req = requests.get(url)
    try:
        req.raise_for_status()
        soup = BeautifulSoup(req.content, 'html.parser')
        obj = []
        for item in soup.find_all('section'):
            obj.append(item.text)
        return obj
    except Exception as exc:
        return f'There was a problem: {exc} '




if __name__ == '__main__':
    pass
