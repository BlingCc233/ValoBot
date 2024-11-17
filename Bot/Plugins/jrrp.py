import base64
import os
import random
import io
import toml
from PIL import Image, ImageDraw, ImageFont

current_path = os.getcwd()

# 检查是否存在 "Assets" 文件夹
assets_folder = os.path.join(current_path, "Assets")
if not os.path.exists(assets_folder) or not os.path.isdir(assets_folder):
    # 切换到上级目录
    parent_path = os.path.dirname(current_path)
    os.chdir(parent_path)


class JRRP:
    def __init__(self, user_id):
        self.user_id = str(user_id)
        self.data_file = '.jrrp.toml'
        self.bg_image_path = 'Assets/img/jrrp_bg.PNG'
        self.font_path = 'Assets/fontFamily.ttf'
        self.data = self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                return toml.load(f)
        return {}

    def save_data(self):
        with open(self.data_file, 'w') as f:
            toml.dump(self.data, f)

    def generate_jrrp(self):
        if self.user_id not in self.data:
            jrrp_value = self.generate_random_jrrp()
            self.data[self.user_id] = self.generate_image(jrrp_value)
            self.save_data()
        return self.data[self.user_id]


    def generate_random_jrrp(self):
        # 生成0-100的整数，概率集中在50-77
        while True:
            value = random.randint(0, 100)
            if 50 <= value <= 77 or random.random() < 0.3:
                return value

    def generate_image(self, jrrp_value):
        bg_image = Image.open(self.bg_image_path)
        draw = ImageDraw.Draw(bg_image)
        font = ImageFont.truetype(self.font_path, 80)
        text = f"今日人品"
        x = 550
        y = 100
        draw.text((x, y), text, fill="#7998A9", font=font)

        font = ImageFont.truetype(self.font_path, 160)
        text = f"{jrrp_value}"
        x = 600
        y = 400
        draw.text((x, y), text, fill="#F5F5F5", font=font)

        # bg_image.save(f"Assets/img/{self.user_id}.png")

        # 将图片转换为Base64
        buffered = io.BytesIO()
        bg_image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        return img_str

    def clear_data(self):
        self.data = {}
        self.save_data()

