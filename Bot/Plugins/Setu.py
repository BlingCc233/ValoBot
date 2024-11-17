import logging

import requests
import json

class Setu():
    def __init__(self, type, keyword):
        self.type = type
        self.keyword = keyword

    def keyword_process(self):
        url = "https://api.lolicon.app/setu/v2"

        if self.type == 1:
            url = url + '?excludeAI=1&size=small&' + self.keyword
            return requests.get(url)

        elif self.type == 2:
            setu_keyword = ['色图', 'setu', '涩图', '瑟图']
            # keyword字符串中不包含任意一个setu_keyword
            if not any(self.keyword.find(i) != -1 for i in setu_keyword):
                return 1

            r18 = 0
            num = 1
            tag = []

            prefix_setu = ['整点', '来张', '来点', '搞点', '我要', '看看', '来份']
            if any(self.keyword.startswith(i) for i in prefix_setu):
                prefix = [i for i in prefix_setu if self.keyword.startswith(i)][0]
                sufix = [i for i in setu_keyword if i in self.keyword][-1]

                # 提取出prefix与setu_keyword之间的文字
                first_proc = self.keyword.split(prefix)[1]
                # 找出setu_keyword中文本真正结尾的那个词

                second_proc = first_proc.split(sufix)[0]
                # 并以,分割成列表
                tag = second_proc.split('，')
                if 'r18' in tag:
                    r18 = 1
                    tag.remove('r18')
                if len(tag) != 0:
                    # 把tag中的每个元素包装成一个单独的列表，并把这些列表放在一个列表中
                    tag = [[i] for i in tag]

                payload = json.dumps({
                    "r18": r18,
                    "tag": tag,
                    "size": "small",
                    "excludeAI": True,
                    "num": num
                })
                headers = {
                    'Content-Type': 'application/json'
                }
                return requests.request("POST", url, headers=headers, data=payload)

            start_word = '给我来'
            if self.keyword.startswith(start_word):
                hanzi_quantity = ['一', '两', '三', '四', '五', '六', '七', '八', '九', '十']
                quantity = self.keyword.split(start_word)[1][0]
                if quantity not in hanzi_quantity:
                    quantity = 1
                elif quantity in hanzi_quantity:
                    quantity = hanzi_quantity.index(quantity) + 1
                num = quantity
                # 从文本中找出"张"与sufix之间的文本
                sufix = [i for i in setu_keyword if i in self.keyword][-1]
                first_proc = self.keyword.split('张')[1]
                second_proc = first_proc.split(sufix)[0]
                tag = second_proc.split('，')
                if 'r18' in tag:
                    r18 = 1
                    tag.remove('r18')
                if len(tag) != 0:
                    # 把tag中的每个元素包装成一个单独的列表，并把这些列表放在一个列表中
                    tag = [[i] for i in tag]

                payload = json.dumps({
                    "r18": r18,
                    "tag": tag,
                    "size": "small",
                    "excludeAI": True,
                    "num": num
                })
                headers = {
                    'Content-Type': 'application/json'
                }
                return requests.request("POST", url, headers=headers, data=payload)

    def setu(self):
        response = self.keyword_process()
        if response == 1:
            return 1
        if response == None:
            return -1
        urls = [i['urls']['small'] for i in response.json()['data']]
        return urls


if __name__ == '__main__':
    print(Setu(2, '').setu())
