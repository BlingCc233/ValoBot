import os
import time

import requests
import json


url = "http://localhost:3000/send_group_msg"

def send_voice(msg):
    payload = json.dumps({
        "group_id": 763934082,
        "message": msg
    })
    headers = {
       'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

if __name__ == '__main__':
    # 定时任务每两小时执行一次
    time.sleep(7200)

    with open('data.txt', 'r') as f:
        lines = f.readlines()

    for line in lines:
        send_voice(line)

    os.remove('data.txt')