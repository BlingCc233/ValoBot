import base64
import collections
import logging
import random
import time

import Plugins
import requests
import Config
from Plugins.jrrp import JRRP
from Plugins.answer import Answer_Book
from Plugins.Setu import Setu
from Plugins.LLM import LLM
from Plugins.text2img import text2img
from Plugins.LLM import DuckDuckGoChat

debug_mode = Config.debug_mode
if debug_mode:
    import shutil
    import os
    import json
    import subprocess

qwen = LLM()
ddg = DuckDuckGoChat()
chat_llm = ddg
msg_stack = {}

port = Config.server_port


class send_private_msg():
    def __init__(self, user_id, message):
        self.user_id = user_id
        self.message = message
        self.url = f"http://localhost:{port}/send_private_msg"

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
        return requests.post(self.url, json=data)

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
        self.url = f"http://localhost:{port}/send_group_msg"

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
            logging.debug(self.message)
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
                response = requests.post(self.url, json=data)
                response = response.json()
                if response['status'] == 'failed':
                    break
            return response['status']
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

    def reply_msg(self, message_id):
        data = {
            "group_id": self.group_id,
            "message": [
                {
                    "type": "reply",
                    "data": {
                        "id": message_id
                    }
                },
                {
                    "type": "text",
                    "data": {
                        "text": self.message
                    }
                }
            ]
        }
        return requests.post(self.url, json=data)

    def send_video(self):
        data = {
            "group_id": self.group_id,
            "message": [
                {
                    "type": "video",
                    "data": {
                        "file": self.message
                    }
                }
            ]
        }
        return requests.post(self.url, json=data)

    def send_group_ai_record(self):
        self.url = f"http://localhost:{port}/send_group_ai_record"
        data = {
            "group_id": self.group_id,
            "character": "lucy-voice-female1",
            "text": self.message
        }
        return requests.post(self.url, json=data)

    def send_record(self):
        data = {
            "group_id": self.group_id,
            "message": [{
                "type": "record",
                "data": {
                    "file": self.message
                }
            }]
        }
        return requests.post(self.url, json=data)


class handle_user_event():
    def __init__(self):
        self.url = f"http://localhost:{port}"

    def get_stranger_info(self, user_id):
        event = "/get_stranger_info"
        data = {
            "user_id": user_id
        }
        return requests.post(self.url + event, json=data)

    def get_user_nickname(self, user_id):
        data = self.get_stranger_info(user_id)
        data = data.json()
        nickname = data['data']['nick']
        return nickname

    def get_msg(self, message_id):
        event = "/get_msg"
        data = {
            "message_id": message_id
        }
        return requests.post(self.url + event, json=data)

    def ban_user(self, group_id, user_id, duration):
        duration = duration * 60
        event = "/set_group_ban"
        data = {
            "group_id": group_id,
            "user_id": user_id,
            "duration": duration
        }
        return requests.post(self.url + event, json=data)

    def send_like(self, user_id):
        event = "/send_like"
        data = {
            "user_id": user_id,
            "times": 10
        }
        return requests.post(self.url + event, json=data)

    def set_essence_msg(self, message_id):
        event = "/set_essence_msg"
        data = {
            "message_id": message_id
        }
        return requests.post(self.url + event, json=data)

    def delete_essence_msg(self, message_id):
        event = "/delete_essence_msg"
        data = {
            "message_id": message_id
        }
        return requests.post(self.url + event, json=data)

    def delete_msg(self, message_id):
        event = "/delete_msg"
        data = {
            "message_id": message_id
        }
        return requests.post(self.url + event, json=data)


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

        if self.data['post_type'] == 'message':
            if self.data['message_type'] == 'group':
                group_id = self.data['group_id']
                # 开一个大小为3的字典栈msg_stack，用于存储每条group_id的消息
                if group_id not in msg_stack:
                    msg_stack[group_id] = collections.deque(maxlen=3)
                    msg_stack[group_id].append(self.raw_message)
                else:
                    msg_stack[group_id].append(self.raw_message)

                if debug_mode:
                    logging.info(msg_stack)

                if len(msg_stack[group_id]) == 3:
                    if msg_stack[group_id][0] == msg_stack[group_id][1] == msg_stack[group_id][2]:
                        # 清空栈
                        msg_stack[group_id].clear()
                        data = {
                            'time': int(time.time()),
                            'self_id': Config.self_id,
                            'post_type': 'notice',
                            'group_id': group_id,
                            'notice_type': 'group_duplicate',
                            'user_id': self.user_id,
                            'message_id': self.message_id + 1
                        }
                        return requests.post(f"http://localhost:{Config.client_port}", json=data)

    def save_bbox(self):
        if 'raw_message' in self.data and random.random() < 0.2:
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
        self.data = data

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
                            raw_message = line.split('å')[1] + f'\n__' + handle_user_event().get_user_nickname(
                                line.split('å')[2])
                            break
            except:
                pass

            send_group_msg('', raw_message).send_raw_msg(self.group_id)

    def no_more_duplicate(self):
        nickname = handle_user_event().get_user_nickname(self.data["user_id"])
        if debug_mode:
            logging.info('no_more_duplicate REC')
            logging.info(self.data["user_id"])
        url = "https://api.tangdouz.com"
        # set nickname
        res = requests.get(url + '/qqname.php', params={'name': nickname, 'qq': self.data["user_id"]})
        if debug_mode:
            logging.info(res.text)
        res = requests.get(url + '/wz/py.php', params={'q': self.data["user_id"], 'nr': "这是什么？+1，点一下"})
        image_data = res.content
        base64_encoded_image = base64.b64encode(image_data).decode('utf-8')
        return send_group_msg(self.group_id, "base64://" + base64_encoded_image).send_img()


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

    # 定义命令， 与开关
    commands = {
        'help': 1,
        'shop': 1,
        'setu': 1,
        'echo': 1,
        'roll': 1,
        'jrrp': 1,
        '签到': 1,
        '赞我': 1,
        '答案': 1,
        '设精': 1,
        '取精': 1,
        'echo_voice': 1,
        'draw': 1,
        '喜报': 1,
        '发电': 1,
        'video': 1,
        '农': 1,
        '抽签': 1,
        'qrcode': 1,
        '放假': 1,

    }

    admin_commands = {
        '禁言': 1,

    }

    def __init__(self, data):
        if 'group_id' in data:
            self.group_id = data['group_id']
        self.user_id = data['user_id']
        self.message_id = data['message_id']
        self.message_type = data['message'][0]['type']
        self.raw_message = data['raw_message']
        self.message = data['message'][0]
        self.data = data
        self.url = f"http://localhost:{port}"

    def group_msg(self):
        if self.raw_message.startswith('/') or self.message_type == 'reply':
            cmd = self.raw_message
            if self.message_type == 'reply':
                for i in self.data['message']:
                    if i['type'] == 'text':
                        cmd = i['data']['text'][1:]
                        break
                if not '/' in cmd:
                    return self.at_or_reply()

            command = cmd.split(' ')[0].strip('/')

            if debug_mode:
                logging.warn("RECIEVED")
                logging.info(command)
            if command not in self.commands and command not in self.admin_commands:
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
                if type(pics) == list:
                    sent = send_group_msg(self.group_id, pics).send_img()
                    if sent == 'failed':
                        send_group_msg(self.group_id, '少🦌一点').send_text()

            elif command == 'echo':
                return send_group_msg('', self.raw_message[6:]).send_raw_msg(self.group_id)

            elif command == 'roll':
                return self.dice()

            elif command == 'jrrp' or command == '签到':
                return send_group_msg(self.group_id, JRRP(self.user_id).generate_jrrp()).send_text_and_pic(
                    f'超天酱的今日份运势🧬( ⁎ᵕᴗᵕ⁎ )🧬:', self.user_id)

            elif command == '赞我':
                response = handle_user_event().send_like(self.user_id)
                data = response.json()
                if data['status'] == 'failed':
                    return send_group_msg('', f'[CQ:at,qq={self.user_id}]\n'
                                              f'今日点赞已达上限').send_raw_msg(self.group_id)
                return send_group_msg(self.group_id, '已为你点赞十次').send_text()

            elif command == '答案':
                return send_group_msg(self.group_id, Answer_Book().get_answer()).reply_msg(self.message_id)

            elif command == "echo_voice":
                return send_group_msg(self.group_id, self.raw_message[12:]).send_group_ai_record()

            elif command == 'draw':
                prompt = ''
                try:
                    prompt = self.raw_message[6:]
                except:
                    pass
                prmpt = text2img(prompt).translate_zh_en()
                send_group_msg(self.group_id,
                               f"Prompt:\n{prmpt}\n由于模型较大，图片生成时间可能比较长，多则几十秒，请耐心等待").reply_msg(
                    self.message_id)
                return send_group_msg(self.group_id, "base64://" + text2img(prompt).get_image(prmpt)).send_img()

            elif command == '喜报':
                content = str(handle_user_event().get_user_nickname(self.user_id)) + "活了"
                try:
                    content = self.raw_message.split(' ')[1]
                except:
                    pass
                data = {
                    "content": content,
                }
                res = requests.get("https://sdk.blingcc.eu.org/api/xb", params=data)
                base64_encoded_image = base64.b64encode(res.content).decode('utf-8')
                return send_group_msg(self.group_id, "base64://" + base64_encoded_image).send_img()

            elif command == '发电':
                nickname = handle_user_event().get_user_nickname(self.user_id)
                res = requests.get("https://api.tangdouz.com/beill.php", params={'name': nickname})
                get_mad = res.text.split(r"\r")
                # 拼接所有get_mad为一个字符串
                get_mad = "\n".join(get_mad)
                return send_group_msg(self.group_id, f"{get_mad}").send_text()

            elif command == 'video':
                res = requests.get("https://api.tangdouz.com/abz/vid.php")
                vid_url = res.text
                return send_group_msg(self.group_id, vid_url).send_video()

            elif command == '农':
                character = '瑶'
                try:
                    character = self.raw_message.split(' ')[1]
                except:
                    pass
                res = requests.get('https://api.tangdouz.com/wzyyb.php', params={'nr': character})
                data = res.json()
                choose = random.randint(1, data['xnum']) - 1
                return send_group_msg(self.group_id, data['data'][choose]['url']).send_record()

            elif command == '抽签':
                res = requests.get("https://sdk.blingcc.eu.org/api/qcs")
                base64_encoded_image = base64.b64encode(res.content).decode('utf-8')
                return send_group_msg(self.group_id, "base64://" + base64_encoded_image).send_img()

            elif command == 'qrcode':
                text = 'V我50'
                try:
                    text = self.raw_message.split(' ')[1]
                except:
                    pass
                res = requests.get("https://sdk.blingcc.eu.org/api/t2qr?text=" + text)
                base64_encoded_image = base64.b64encode(res.content).decode('utf-8')
                return send_group_msg(self.group_id, "base64://" + base64_encoded_image).send_img()

            elif command == '放假':
                res = requests.get("https://sdk.blingcc.eu.org/api/holiday")
                return send_group_msg(self.group_id, res.text).send_text()



            elif command == '禁言':
                if self.user_id != Config.admin:
                    return send_group_msg(self.group_id, '你没有禁言的权限').send_text()
                ban_id, ban_dur = '', ''
                try:
                    ban_id = self.data['message'][1]['data']['qq']
                    ban_dur = self.data['message'][2]['data']['text']
                except:
                    pass
                if ban_id == '' or ban_dur == '':
                    return send_group_msg(self.group_id, f'参数格式错误或参数不足\n'
                                                         f'禁言格式为：/禁言 @禁言对象 禁言时长(分钟)').send_text()
                return handle_user_event().ban_user(self.group_id, int(ban_id), int(ban_dur))

            elif command == '设精':
                if not self.message_type == 'reply':
                    return send_group_msg(self.group_id, '请回复需要精华的消息').send_text()
                essence_msg = self.message['data']['id']
                return handle_user_event().set_essence_msg(int(essence_msg))

            elif command == '取精':
                if not self.message_type == 'reply':
                    return send_group_msg(self.group_id, '请回复需要取消精华的消息').send_text()
                essence_msg = self.message['data']['id']
                response = handle_user_event().delete_essence_msg(int(essence_msg))
                data = response.json()
                if data['status'] == 'ok':
                    return send_group_msg(self.group_id, '已取消精华').send_text()

            return

        if self.is_at_me() or self.is_reply_me():
            return self.at_or_reply()


        else:
            self.handle_keyword()

        return

    def private_msg(self):
        global chat_llm
        if self.user_id == Config.admin:
            if self.raw_message == 'recall 1':
                Config.is_recall = True
                return send_private_msg(self.user_id, '已开启撤回检测').send_text()
            elif self.raw_message == 'recall 0':
                Config.is_recall = False
                return send_private_msg(self.user_id, '已关闭撤回检测').send_text()
            elif self.raw_message == 'debug 1':
                Config.is_debug = True
                return send_private_msg(self.user_id, '已开启调试模式').send_text()
            elif self.raw_message == 'debug 0':
                Config.is_debug = False
                return send_private_msg(self.user_id, '已关闭调试模式').send_text()
            elif self.raw_message == 'llm qwen':
                ddg.user_sessions = {}
                chat_llm = qwen
                return send_private_msg(self.user_id, '目前模型：Qwen/Qwen2.5-Coder-32B-Instruct').send_text()
            elif self.raw_message == 'llm ddg':
                qwen.conversation_history = {}
                chat_llm = ddg
                return send_private_msg(self.user_id, '目前模型：DuckDuckGo/gpt-4o-mini').send_text()

        if self.user_id in Config.user_black_list:
            return

        else:
            if "新早苗" in self.raw_message:
                chat_llm.new_conversation(self.user_id)
                return send_private_msg(self.user_id, '已经换上新早苗了').send_text()

            take_time = send_private_msg(self.user_id, '对方正在输入...').send_text()
            take_time = take_time.json()
            just_msg = take_time['data']['message_id']
            response = chat_llm.get_response(self.raw_message, self.user_id)
            handle_user_event().delete_msg(just_msg)
            return send_private_msg(self.user_id, response).send_text()

        return

    def handle_keyword(self):
        pics = Setu(2, self.raw_message).setu()
        if type(pics) == list:
            sent = send_group_msg(self.group_id, pics).send_img()
            if sent == 'failed':
                send_group_msg(self.group_id, '少🦌一点').send_text()
            return

        # 处理关键词
        keyword_reply = {
            '晚安': '晚安喵～',
            'oi': 'Oi~',
            '那我问你': '你头怎么尖尖的',
            '打b': 'poh',
            '宝': '宝宝在吗',
            '早上好': '早上好说是',
            f'[CQ:at,qq={Config.admin}]': '叫我主人干嘛',
            'NB': '包的',
            '不是哥们': '布什戈门',
            '瓦吗': '上号',
            '打哇': '你先开',
            '哇吗': '来',
        }
        # 从keyword_reply的键中找出存在于raw_message中的关键词
        if [i for i in keyword_reply.keys() if i in self.raw_message]:
            keyword = [i for i in keyword_reply.keys() if i in self.raw_message][0]
            # logging.info(keyword)
            reply = keyword_reply[keyword]
            send_group_msg(self.group_id, reply).send_text()
            return

        return

    def at_or_reply(self):
        if self.is_at_me() or self.is_reply_me():
            if debug_mode:
                logging.info('RECIEVED')

            user_input = -1
            for i in self.data['message']:
                if i['type'] == 'text':
                    user_input = i['data']['text']
                    break

            if user_input == -1:
                # 单纯at
                return send_group_msg(self.group_id, f"喵喵喵").send_text()

            if "新早苗" in user_input:
                chat_llm.new_conversation(self.user_id)
                return send_group_msg(self.group_id, "已经换上新早苗了").reply_msg(self.message_id)

            take_time = send_group_msg(self.group_id, '猫粮动脑筋中...').send_text()
            take_time = take_time.json()
            just_msg = take_time['data']['message_id']
            response = chat_llm.get_response(user_input, self.user_id)
            handle_user_event().delete_msg(just_msg)
            send_group_msg(self.group_id, response).reply_msg(self.message_id)
            send_group_msg(self.group_id, response).send_group_ai_record()

            return

    # 历史遗留方法，暂时放在这里
    def valo_shop(self):
        shop = Plugins.valo_shop.get_shop(self.user_id)
        if shop == None:
            send_group_msg(self.group_id, '登录掌瓦时出问题了').send_text()
            return
        # logging.info(shop)
        send_group_msg(self.group_id, shop).send_text_and_pic("每日商店", self.user_id)

    def dice(self):
        url = self.url + '/send_group_msg'
        data = {
            'group_id': self.group_id,
            'message': [{
                'type': 'dice',
                'data': {
                    'result': random.randint(1, 6)
                }
            }]
        }
        return requests.post(url, json=data)

    def is_at_me(self):
        return f'[CQ:at,qq={Config.self_id}]' in self.raw_message

    def is_reply_me(self):
        if not self.message_type == 'reply':
            return False
        reply_message_id = self.message['data']['id']
        response = handle_user_event().get_msg(reply_message_id)
        data = response.json()
        return data['data']['sender']['user_id'] == Config.self_id


def handle(data):
    if 'group_id' in data:  # 千万别改
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
        elif data['notice_type'] == 'group_duplicate':
            handle_notice(data).no_more_duplicate()
        return

    cache_data(data).save_cache()

    if data['post_type'] == 'message':
        if data['message_type'] == 'group':
            handle_msg(data).group_msg()
            return
        if data['message_type'] == 'private':
            handle_msg(data).private_msg()
            return
