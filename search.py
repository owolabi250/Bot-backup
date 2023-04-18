import requests

url = "https://rapidprod-sendgrid-v1.p.rapidapi.com/mail/send"

payload = {
	"personalizations": [
		{
			"to": [{"email": "adavaonimisi@gmail.com"}],
			"subject": "testing"
		}
	],
	"from": {"email": "oadava@gmail.com"},
	"content": [
		{
			"type": "text/plain",
			"value": "testing"
		}
	]
}
headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": "9408d13729mshac2279313eb9bbap1eeca0jsne928bf83645e",
	"X-RapidAPI-Host": "rapidprod-sendgrid-v1.p.rapidapi.com"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)
