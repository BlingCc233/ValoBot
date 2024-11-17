import logging
import random

import Plugins
import requests
import Config

from Plugins.Setu import Setu

debug_mode = Config.debug_mode
if debug_mode:
    import shutil
    import os
    import json
    import subprocess


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

    def send_img(self):
        # 判断message如果是一个长度大于1的列表，就发送列表中的所有图片，否则就发送单个图片
        if type(self.message) == list:
            for url in self.message:
                data = {
                    'group_id': self.group_id,
                    'message': [{
                        'type': 'image',
                        'data': {
                            'file': url
                        }
                    }]
                }
                requests.post(self.url, json=data)
            return
        else:
            data = {
                'group_id': self.group_id,
                'message': [{
                    'type': 'image',
                    'data': {
                        'file': str(self.message)
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

class cache_data():
    def __init__(self, data):
        self.message_id = data['message_id']
        self.user_id = data['user_id']
        if 'raw_message' in data:
            self.raw_message = data['raw_message']
        else:
            self.raw_message = ''
        self.data = data

    def save_cache(self):
        if 'raw_message' in self.data:
            with open('Assets/data/data.txt', 'a') as f:
                f.write(str(self.message_id) + 'å' + self.data['raw_message'] + 'å' + str(self.user_id) + '\n')
        # data最多存1000条，就删除最旧的那一条
        if len(open('Assets/data/data.txt', 'r').readlines()) > 1000:
            with open('Assets/data/data.txt', 'r') as f:
                lines = f.readlines()
                lines.pop(0)
            with open('Assets/data/data.txt', 'w') as f:
                f.writelines(lines)
                logging.info('Cache saved')

    def save_bbox(self):
        if 'raw_message' in self.data:
            with open('OtherUse/data.txt', 'a') as f:
                f.write(str(self.raw_message) + '\n')

        # 当data最多存1000条，就删除最旧的那一条
        if len(open('OtherUse/data.txt', 'r').readlines()) > 1000:
            with open('OtherUse/data.txt', 'r') as f:
                lines = f.readlines()
                lines.pop(0)
            with open('OtherUse/data.txt', 'w') as f:
                f.writelines(lines)
                logging.info('Cache saved')

class handle_notice():
    def __init__(self, data):
        self.group_id = data['group_id']
        self.message_id = data['message_id']

    def anti_recall(self):
        if debug_mode:
            logging.info('anti_recall REC')
        if Config.is_recall:
            # 对于已经撤回的消息，从Assests/data/data.txt中读取与data['message_id']相同的message_id的raw_message
            try:
                with open('Assets/data/data.txt', 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        if line.split('å')[0] == str(self.message_id):
                            raw_message = line.split('å')[1] + f'\n__' + handle_user_event(line.split('å')[2]).get_user_nickname()
                            break
            except:
                pass

            send_group_msg('', raw_message).send_raw_msg(self.group_id)

class handle_msg():
    # 定义枚举量，message_type
    message_type = {
        'text': 0,
        'image': 1,
        'face': 2,
        'at': 3,
        'at_me': 4,
        'record': 5,
        'video': 6,
        'file': 7,
        'location': 8,
        'music': 9,
        'share': 10,
        'xml': 11,
        'json': 12,
        'node': 13,
        'reply': 14,
    }

    # 定义枚举量,命令类型
    commands = {
        'help': 0,
        'shop': 1,
        'setu': 2,
        'echo': 3,
        'roll': 4,
    }

    def __init__(self, data):
        if 'group_id' in data:
            self.group_id = data['group_id']
        self.user_id = data['user_id']
        self.message_id = data['message_id']
        self.message_type = data['message'][0]['type']
        self.raw_message = data['raw_message']
        self.message = data['message'][0]
        self.url = "http://localhost:3000"

    def group_msg(self):
        if self.message_type == 'text' and self.raw_message.startswith('/'):
            command = self.raw_message.split(' ')[0].strip('/')

            if debug_mode:
                logging.warn("RECIEVED")
                logging.info(command)
            if command not in self.commands:
                return send_group_msg(self.group_id, '暂不支持的命令').send_text()
            if command == 'help':
                return send_group_msg(self.group_id, f'\tValo✨Bot v{Config.version}\n'
                                                     f'❕命令应以"/"开头，如：/help\n'
                                                     f'目前支持的命令有:\n'
                                                     f'{list(self.commands.keys())}').send_text()
            elif command == 'shop':
                return self.valo_shop()
            elif command == 'setu':
                keyword = ''
                try:
                    keyword = self.raw_message.split(' ')[1]
                except:
                    pass
                pics = Setu(1, keyword).setu()
                if pics == -1:
                    send_group_msg(self.group_id, '少🦌一点').send_text()
                else:
                    send_group_msg(self.group_id, pics).send_img()
            elif command == 'echo':
                return send_group_msg('', self.raw_message[6:]).send_raw_msg(self.group_id)
            elif command == 'roll':
                try:
                    num = int(self.raw_message.split(' ')[1])
                except:
                    num = None
                    pass
                return self.dice(num)
            return

        if self.message_type == 'at' and self.message['data']['qq'] == str(Config.self_id):
            if debug_mode:
                logging.info('RECIEVED')
            reply_words = ['你才是猫娘～', '叫我干嘛', '你干嘛～', '在', '？', '??']
            reply_word = random.choice(reply_words)
            send_group_msg('', f'[CQ:at,qq={self.user_id}]\n'
                               f'{reply_word}').send_raw_msg(self.group_id)
            return

        else:
            self.handle_keyword()


        return

    def private_msg(self):
        if self.user_id == Config.admin:
            if self.raw_message == 'recall 1':
                Config.is_recall = True
                send_private_msg(self.user_id, '已开启撤回检测').send_text()
            elif self.raw_message == 'recall 0':
                Config.is_recall = False
                send_private_msg(self.user_id, '已关闭撤回检测').send_text()
        return

    def valo_shop(self):
        shop = Plugins.valo_shop.get_shop(self.user_id)
        if shop == None:
            send_group_msg(self.group_id, '登录掌瓦时出问题了').send_text()
            return
        logging.info(shop)
        send_group_msg(self.group_id, shop).send_text_and_pic("每日商店", self.user_id)

    def handle_keyword(self):
        pics = Setu(2, self.raw_message).setu()
        if pics == -1:
            send_group_msg(self.group_id, '少🦌一点').send_text()
        else:
            send_group_msg(self.group_id, pics).send_img()

        return

    def dice(self, result):
        url = self.url + '/send_group_msg'
        if result == None or result > 6:
            result = random.randint(1, 6)
        data = {
            'group_id': self.group_id,
            'message': [{
                'type': 'dice',
                'data': {
                    'result': result
                }
            }]
        }
        return requests.post(url, json=data)




def handle(data):
    if 'group_id' in data: # 千万别改
        if data['group_id'] in Config.listen_on_group_list and data['message'][0]['type'] == 'record':
            cache_data(data).save_bbox()
            return
        if data['group_id'] not in Config.group_white_list:
            return



    if (data['user_id'] not in Config.user_white_list and debug_mode) or data['user_id'] in Config.user_black_list:
        return

    if data['post_type'] == 'notice':
        if data['notice_type'] == 'group_recall':
            handle_notice(data).anti_recall()
        return

    cache_data(data).save_cache()


    if data['post_type'] == 'message':
        if data['message_type'] == 'group':
            handle_msg(data).group_msg()
            return
        if data['message_type'] == 'private':
            handle_msg(data).private_msg()
            return




    # 历史遗留问题
    '''
    if data['group_id'] == 701436956 and data['message'][0]['type'] == 'record':
        cache_data(data).save_bbox()
        # nmd = {
        #     "message": str(data['raw_message'])
        # }
        # # 将字典写入 JSON 文件
        # with open('OtherUse/nmd.json', 'w') as file:
        #     json.dump(nmd, file, indent=4)
        #
        # # 工作目录切换到 OtherUse
        # os.chdir('OtherUse')
        # from OtherUse.voice_forward import send_voice
        # send_voice(nmd['message'])
        # os.system("python3.11 voice_forward.py")
        # os.chdir('..')

        # TODO
        bash_command = f"python3.11 OtherUse/voice_forward.py '{data['raw_message']}'"
        # 用bash 执行命令
    '''




