import requests
import os
from requests.structures import CaseInsensitiveDict


def is_valid(email: str):
    url = f"https://api.emailvalidation.io/v1/info?email={email}"

    headers = CaseInsensitiveDict()
    headers['apikey'] = os.environ.get('MAIL_VALIDATE')

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        json_resp = response.json()
        format_valid = json_resp['format_valid']
        mx_found = json_resp['mx_found']
        smtp_check = json_resp['smtp_check']
        state = json_resp['state']

        return format_valid and mx_found and smtp_check and state == 'deliverable'

    return False

