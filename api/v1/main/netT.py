import smtplib
import os
import wikipedia
import requests
from cachetools import TTLCache
import os

cache = TTLCache(maxsize=100, ttl=300)
wikipedia.set_lang('en')

def send_email(user):
    try:
        sender_email = os.environ.get('MAIL_USERNAME')
        port = os.environ.get('MAIL_PORT')
        myserver = os.environ.get('MAIL_SERVER')
        passK = os.environ.get('MAIL_PASSWORD')
        token = user.generate_confirmation_code()
        code = token[0]
        receiver_email = user.Email
        msg = f"""<p>Before we change the email on your account,
                we just need to confirm that this is you. 
                Below is the verification code for your Discord account.
                {code}
                Don't share this code with anyone.
                If you didn't ask for this code, please ignore this email </p>.
            """
        with smtplib.SMTP(myserver, port) as server:
            server.starttls()
            server.login(sender_email, passK)
            server.sendmail(sender_email, receiver_email, msg)
            print("Email sent successfully")
    except Exception as e:
        return f"some error occured {e}"

def search(text):
    # check if the search term is in the cache
    if text in cache:
        summary = cache[text]
    else:
        # check if the search term is spelled correctly
        suggestion = wikipedia.suggest(text)
        if suggestion:
            text = suggestion
    # get the search results
    results = wikipedia.search(text, results=5)
    # get the page summary of the first search result
    page = wikipedia.page(results[0])

    summary = page.summary 
    # add the search term and summary to the cache
    cache[text] = summary
    # print the summary
    return summary

def get_wiki_briefs(query):

    url = "https://wiki-briefs.p.rapidapi.com/search"

    querystring = {"q":query,"topk":"3"}
    code = os.environ.get('RapidAPI')
    Host = os.environ.get('X-RapidAPI-Host')
    code = str(code)
    headers = {
	    "X-RapidAPI-Key": code,
	    "X-RapidAPI-Host": Host
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    if response.status_code == 200:
        response_dict = response.json()
        return response_dict
    else:
        return None
