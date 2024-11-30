import json
import io
import base64
import logging
import random

from PIL import Image
from g4f.client import Client
from g4f.Provider import ReplicateHome
from huggingface_hub import InferenceClient
from Plugins.llm_config import api_key
import requests


class trans_zh_en:
    def __init__(self):
        self.client = InferenceClient(api_key=api_key)
        # self.client = Client()
        self.messages = [
            {
                "role": "system",
                # "content": "下面我让你来充当翻译家，你的目标是把任何语言翻译成英文，请翻译时不要带翻译腔，而是要翻译得自然、流畅和地道，使用优美和高雅的表达方式。"
                "content": (
                    "从现在开始，你是一名中英翻译，你会根据我输入的中文内容，翻译成对应英文。请注意，你翻译后的内容主要服务于一个绘画AI，它只能理解具象的描述而非抽象的概念，同时根据你对绘画AI的理解，比如它可能的训练模型、自然语言处理方式等方面，进行翻译优化。由于我的描述可能会很散乱，不连贯，你需要综合考虑这些问题，然后对翻译后的英文内容再次优化或重组，从而使绘画AI更能清楚我在说什么。请严格按照此条规则进行翻译，也只输出翻译后的英文内容。 例如，我输入：“一只想家的小狗”"
                    "你不能输出："
                    "A homesick little dog."
                    "你必须输出："
                    "A small dog that misses home, with a sad look on its face and its tail tucked between its legs.It might be standing in front of a closed door or a gate, gazing longingly into the distance, as if hoping to catch a glimpse of its beloved home."
                    "注意，你翻译后的内容不应过长，简单扩展联想即可"
                    "当我输入中文内容后，请翻译我需要的英文内容。翻译后的内容中不可以出现中文。")
            }
        ]

    def translate(self, text):
        self.messages.append({
            "role": "user",
            "content": text
        })

        completion = self.client.chat.completions.create(
            seed=random.randint(0, 100000),
            model="Qwen/Qwen2.5-Coder-32B-Instruct",
            messages=self.messages,
            max_tokens=700
        )

        translated_text = completion.choices[0].message.content
        return translated_text


class text2img:
    def __init__(self, zh_prompt):
        # self.client = InferenceClient("Nishitbaria/Anime-style-flux-lora-Large", token=api_key)
        self.client = Client()
        self.prompt = "Animeo, Anime, "
        self.zh_prompt = zh_prompt
        self.negative_prompt = "nsfw, paintings, cartoon, anime, sketches, worst quality, low quality, normal quality, lowres, watermark, monochrome, grayscale, ugly, blurry, Tan skin, dark skin, black skin, skin spots, skin blemishes, age spot, glans, disabled, bad anatomy, amputation, bad proportions, twins, missing body, fused body, extra head, poorly drawn face, bad eyes, deformed eye, unclear eyes, cross-eyed, long neck, malformed limbs, extra limbs, extra arms, missing arms, bad tongue, strange fingers, mutated hands, missing hands, poorly drawn hands, extra hands, fused hands, connected hand, bad hands, missing fingers, extra fingers, 4 fingers, 3 fingers, deformed hands, extra legs, bad legs, many legs, more than two legs, bad feet, extra feets, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry"

    def translate_zh_en(self):
        translator = trans_zh_en()
        english_text = translator.translate(self.zh_prompt)
        return english_text

    def get_image(self, prmpt):
        if prmpt != "":
            en_prompt = prmpt
        else:
            en_prompt = self.translate_zh_en()
        self.prompt = self.prompt + en_prompt
        print(self.prompt)
        response = self.client.images.generate(
            model="playgroundai/playground-v2.5-1024px-aesthetic",
            prompt=self.prompt,
            provider=ReplicateHome,
        )
        image_path = response.data[0].url
        # 文件在generated_images/
        image_path = image_path.split('/')[2]
        print(f"Generated image PATH: {image_path}")

        image = Image.open(f"generated_images/{image_path}")

        # image = self.client.text_to_image(prompt=self.prompt, seed=random.randint(0, 100000), width=768, height=768, num_inference_steps=16)
        # 保存图片到test/
        # image.save("test/test.png")
        # 转为base64
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        return image_base64


if __name__ == "__main__":
    zh_prompt = "[Anime girl with teal hair, holding a love letter, slightly anxious and determined expression, slightly sweaty], [Digital painting, anime style], [Inspired by the style of various VTuber artists, a blend of soft and sharp lines], [Soft lighting, pastel color palette with teal, pink, and yellow accents, slightly desaturated colors, focus on the character's face, slightly blurred background, smooth rendering, subtle texture on the hair]"
    image_base64 = text2img(zh_prompt).get_image("")

    # print(image_base64)
