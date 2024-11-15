import logging
import Plugins
import requests
import Config
import subprocess

debug_mode = Config.debug_mode
if debug_mode:
    import shutil
    import os
    import json


class send_private_msg():
    def __init__(self, user_id, message):
        self.user_id = user_id
        self.message = message
        self.url = "http://localhost:3000/send_private_msg"
    def send_text(self):
        print(self.url)
        data = {
            'user_id': self.user_id,
            'message': [{
                'type': 'text',
                'data': {
                    'text': str(self.message)
                }
            }]
        }
        requests.post(self.url, json=data)

    def send_image(self):
        data = {
            'group_id': self.group_id,
            'message': [{
                'type': 'image',
                'data': {
                    'file': 'file:// ./{0}'.format(self.message)
                }
            }]
        }
        requests.post(self.url, json=data)

class send_group_msg():
    def __init__(self, group_id, message):
        self.group_id = group_id
        self.message = message
        self.url = "http://localhost:3000/send_group_msg"

    def send_raw_msg(self, group_id):
        data = {
            'group_id': group_id,
            'message': self.message
        }
        return requests.post(self.url, json=data)

    def send_text(self):
        data = {
            'group_id': self.group_id,
            'message': [{
                'type': 'text',
                'data': {
                    'text': str(self.message)
                }
            }]
        }
        return requests.post(self.url, json=data)

    def send_text_and_pic(self, text_msg, user_id):
        data = {
            "group_id": self.group_id,
            "message": [
                {
                    "type": "at",
                    "data": {
                        "qq": user_id
                    }
                },
                {
                    "type": "text",
                    "data": {
                        "text": f"\n{text_msg}"
                    }
                },
                {
                    "type": "image",
                    "data": {
                        "file": "base64://{0}".format(self.message)
                    }
                }
            ]
        }
        return requests.post(self.url, json=data)

class handle_user_event():
    def __init__(self, user_id):
        self.user_id = user_id
        self.url = "http://localhost:3000"

    def get_stranger_info(self):
        event = "/get_stranger_info"
        data = {
            "user_id": self.user_id
        }
        return requests.post(self.url + event, json=data)

    def get_user_nickname(self):
        data = self.get_stranger_info()
        data = data.json()
        nickname = data['data']['nick']
        return nickname


def save_cache(data):
    if 'raw_message' in data:
        with open('Assets/data/data.txt', 'a') as f:
            f.write(str(data['message_id']) + 'å' + data['raw_message'] + 'å' + str(data['user_id']) + '\n')

    #当data最多存1000条，就删除最旧的那一条
    if len(open('Assets/data/data.txt', 'r').readlines()) > 1000:
        with open('Assets/data/data.txt', 'r') as f:
            lines = f.readlines()
            lines.pop(0)
        with open('Assets/data/data.txt', 'w') as f:
            f.writelines(lines)
            logging.info('Cache saved')

def save_bbox(data):
    if 'raw_message' in data:
        with open('OtherUse/data.txt', 'a') as f:
            f.write(data['raw_message'] + '\n')

    #当data最多存1000条，就删除最旧的那一条
    if len(open('OtherUse/data.txt', 'r').readlines()) > 1000:
        with open('OtherUse/data.txt', 'r') as f:
            lines = f.readlines()
            lines.pop(0)
        with open('OtherUse/data.txt', 'w') as f:
            f.writelines(lines)
            logging.info('Cache saved')

def handle(data):
    if data['user_id'] not in Config.user_white_list and debug_mode:
        return
    if 'group_id' in data:
        if data['group_id'] not in Config.group_white_list:
            logging.info(data)

            if data['group_id'] == 309887999 and data['message'][0]['type'] == 'record' and data['post_type'] == 'message':
                save_bbox(data)
            return

    save_cache(data)


    if data['post_type'] == 'notice' and data['notice_type'] == 'group_recall':
        #对于已经撤回的消息，从Assests/data/data.txt中读取与data['message_id']相同的message_id的raw_message
        with open('Assets/data/data.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.split('å')[0] == str(data['message_id']):
                    raw_message = line.split('å')[1] + f'\n__' + handle_user_event(line.split('å')[2]).get_user_nickname()
                    break

        send_group_msg(data['group_id'], raw_message).send_text()
        return

    if debug_mode:
        logging.info(data)

    if data['post_type'] == 'message':
        if data['message'][0]['type'] == 'text' and data['message'][0]['data']['text'].startswith('/'):
            logging.debug('Recieved....')

            command = data['message'][0]['data']['text'].split(' ')
            if command[0] == '/test':
                shop = Plugins.valo_shop.get_shop(data['user_id'])
                if shop == None:
                    send_group_msg(data['group_id'], '登录掌瓦时出问题了').send_text()
                logging.info(shop)
                send_group_msg(data['group_id'], shop).send_text_and_pic("每日商店", data['user_id'])



            if data['message_type'] == 'group':
                if debug_mode and data['group_id'] == Config.group_id:
                    logging.debug('Recieved....')

        if data['group_id'] == 701436956 and data['message'][0]['type'] == 'record':
            nmd = {
                "message": str(data['raw_message'])
            }
            # 将字典写入 JSON 文件
            with open('OtherUse/nmd.json', 'w') as file:
                json.dump(nmd, file, indent=4)

            # 工作目录切换到 OtherUse
            os.chdir('OtherUse')
            from OtherUse.voice_forward import send_voice
            send_voice(nmd['message'])
            os.system("python3.11 voice_forward.py")
            os.chdir('..')



