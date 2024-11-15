import os

import requests
import json


current_path = os.getcwd()
print(current_path)
# 打开并保存nmd.json
with open('nmd.json', 'r') as f:
    nmd = json.load(f)

url = "http://localhost:3000/send_group_msg"

def send_voice(msg):
    payload = json.dumps({
        "group_id": 701436956,
        "message": msg
    })
    headers = {
       'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

if __name__ == '__main__':
    send_voice(nmd['message'])