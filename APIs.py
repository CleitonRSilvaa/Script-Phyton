import requests
import json
import urllib3
import os
from dotenv import load_dotenv
import hmac
import hashlib
import base64



load_dotenv()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url_default = os.getenv('url_default')
# url_update_person = os.getenv('url_update_person')
# url_aplay_person = os.getenv('url_applay_person')
# url_Search_person = os.getenv('url_Search_person')

headers_str = os.getenv('headers')
headers = json.loads(headers_str)

host_hcp = "https://192.168.0.150"
app_key = "22564995"
app_secret = "vkeLZ1bgn2lfBh550lGz"


url_default = "/artemis/api/common/v1/version"
url_update_person = "/artemis/api/resource/v1/person/single/update"
url_applay_person = "/artemis/api/visitor/v1/auth/reapplication"
url_Search_person = "/artemis/api/resource/v1/person/advance/personList"

def gerar_signature(app_secret, mgs):
    message = bytes(mgs, 'utf-8')
    key = bytes(app_secret, 'utf-8')
    hash = hmac.new(key, message, digestmod=hashlib.sha256).digest()
    signature = base64.b64encode(hash)
    return signature.decode()
def message_to_encrypt(request_path):
    mgs = f"POST\n" \
          f"application/json\n" \
          f"application/json;charset=UTF-8\n" \
          f"{request_path}"
    return mgs

def gerenate_headers(p_app_key, p_app_secret, p_url_part):
    mgs = message_to_encrypt(p_url_part)
    signature = gerar_signature(p_app_secret, mgs)
    headers = {'Content-Type': 'application/json;charset=UTF-8',
               'Accept': 'application/json',
               'X-Ca-Key': f'{p_app_key}',
               'X-Ca-Signature': f'{signature}',
               }
    return headers


def search_person(str_nome):
    headers_search_person = gerenate_headers(p_app_key=app_key, p_app_secret=app_secret,
                                             p_url_part=url_Search_person)
    boby = {
        "pageNo": 1,
        "pageSize": 1,
        "personName": str_nome
    }
    response = requests.post(f"{host_hcp}{url_Search_person}", headers=headers_search_person, json=boby, verify=False)
    data_dict = json.loads(response.content)
    data = data_dict["data"]
    if data["total"] >= 1:
        lista = data["list"][0]
        person_id = lista["personId"]
        person_matri = lista["personCode"]
        person_name = lista["personName"]
        return person_id,person_matri,person_name
    return False


def update_person(boby):
    headers_UpdatePerson = gerenate_headers(p_app_key=app_key, p_app_secret=app_secret,
                                            p_url_part=url_update_person)

    response = requests.post(f"{host_hcp}{url_update_person}", headers=headers_UpdatePerson, json=boby, verify=False)
    data_dict = json.loads(response.content)
    return data_dict['msg']

def applay_person():
    headers_aplay_person = gerenate_headers(p_app_key=app_key, p_app_secret=app_secret,
                                            p_url_part=url_applay_person)

    response = requests.post(f"{host_hcp}{url_applay_person}", headers=headers_aplay_person, verify=False)
    data_dict = json.loads(response.content)
    return data_dict['msg']

def connect_api():
    response = requests.post(f"{host_hcp}{url_default}", headers=gerenate_headers(p_app_key=app_key, p_app_secret=app_secret,
                                            p_url_part=url_default), verify=False)
    if response.status_code == 200:
        return True
    elif response.status_code == 404:
        return False
    else:
        return response.json()


if __name__ == '__main__':
    ...