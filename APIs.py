import requests
import json
import urllib3
import os
from dotenv import load_dotenv

load_dotenv()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url_default = os.getenv('url_default')
url_update_person = os.getenv('url_update_person')
url_aplay_person = os.getenv('url_applay_person')

headers_str = os.getenv('headers')
headers = json.loads(headers_str)

headers_applay_str = os.getenv('headers_applay')
headers_applay = json.loads(headers_applay_str)





def update_person(boby):
    response = requests.post(url_update_person, headers=headers, json=boby, verify=False)
    data_dict = json.loads(response.content)
    return data_dict['msg']

def applay_person():
    response = requests.post(url_aplay_person, headers=headers_applay, verify=False)
    data_dict = json.loads(response.content)
    return data_dict['msg']

def connect_api():
    response = requests.post(url_default, headers=headers, verify=False)
    if response.status_code == 200:
        return True
    elif response.status_code == 404:
        return False
    else:
        return response.json()

