import requests


def main():
    url = "https://telesign-telesign-send-sms-verification-code-v1.p.rapidapi.com/sms-verification-code"

    phoneNo = '+22349012391474'
    code = '8080'
    querystring = {"phoneNumber":phoneNo,"verifyCode":code}

    headers = {
	    "X-RapidAPI-Key": "9408d13729mshac2279313eb9bbap1eeca0jsne928bf83645e",
	    "X-RapidAPI-Host": "telesign-telesign-send-sms-verification-code-v1.p.rapidapi.com"
    }

    response = requests.request("POST", url, headers=headers, params=querystring)
    return response.text


def GPT():

    url = "https://openai80.p.rapidapi.com/chat/completions"

    payload = {
	    "model": "gpt-3.5-turbo",
	    "messages": [
		    {
			    "role": "user",
			    "content": "Hello!"
		    }
	    ]
    }
    headers = {
	    "content-type": "application/json",
	    "X-RapidAPI-Key": "9408d13729mshac2279313eb9bbap1eeca0jsne928bf83645e",
	    "X-RapidAPI-Host": "openai80.p.rapidapi.com"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    return response.text

def Aeona(text):

    url = "https://aeona3.p.rapidapi.com/"

    querystring = {"text":text,"userId":"12312312312"}

    headers = {
    	"X-RapidAPI-Key": "9408d13729mshac2279313eb9bbap1eeca0jsne928bf83645e",
	    "X-RapidAPI-Host": "aeona3.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)


    return response.text

if __name__ == '__main__':
    obj = Aeona("Hello")
    print(obj)

