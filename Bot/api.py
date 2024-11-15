import logging
import Plugins
import requests
import Config

debug_mode = Config.debug_mode
if debug_mode:
    import shutil
    import os

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

    def send_text(self):
        data = {
            'group_id': 701436956,
            'message': [{
                'type': 'text',
                'data': {
                    'text': 'Hello, World!'
                }
            }]
        }
        return requests.post(self.url, json=data)


    def send_record(self):
        data = {
            'group_id': self.group_id,
            'message': [{
                'type': 'record',
                'data': {
                    'file': 'file://./{0}'.format(self.message)
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



def handle(data):
    if data['user_id'] not in Config.user_white_list:
        return
    if 'group_id' in data:
        if data['group_id'] not in Config.group_white_list:
            return
    if data['post_type'] == 'notice':
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
                if debug_mode and str(data['group_id']) == '701436956':
                    logging.debug('Recieved....')
                    send_group_msg(data['group_id'], 'Plugins/test/remind.mp3').send_record()

