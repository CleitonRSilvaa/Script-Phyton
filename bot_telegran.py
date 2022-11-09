import requests
import os
from dotenv import load_dotenv
load_dotenv()

def send_message(msg):
    chat_id = os.getenv('KEY-CHAT_ID')
    token = os.getenv('KEY-TOKEN_CODE')
    try:
        data = {"chat_id": chat_id, "text": msg}
        url = "https://api.telegram.org/bot{}/sendMessage".format(token)
        requests.post(url, data)
    except Exception as e:
        print("Erro no sendMessage:", e)
