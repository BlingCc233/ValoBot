import base64
import http
import json
import os
import shutil

import requests
from PIL import Image, ImageDraw, ImageFont

#判断当前工作路径下是否有Assets文件夹，当前工作路径下如果不存在Assets就切换工作路径为上级目录
current_path = os.getcwd()

# 检查是否存在 "Assets" 文件夹
assets_folder = os.path.join(current_path, "Assets")
if not os.path.exists(assets_folder) or not os.path.isdir(assets_folder):
    # 切换到上级目录
    parent_path = os.path.dirname(current_path)
    os.chdir(parent_path)


def download_image(url, user_id,filename):
    response = requests.get(url)
    with open('Assets/img/'+str(user_id)+'/'+filename, 'wb') as file:
        file.write(response.content)

def get_shop(user_id):
    url = "https://app.mval.qq.com/go/mlol_store/agame/user_store"

    headers = {
        "Accept": "*/*",
        "Upload-Draft-Interop-Version": "5",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/json",
        "Content-Length": "231",
        "User-Agent": "mval/1.6.0 (iPhone; IOS 18.0.1; Scale/2.00)",
        "Connection": "keep-alive",
        "Upload-Complete": "?1",
        "GH-HEADER": "1-2-105-160-0",
        "Cookie": "acctype=qc; userId=JA-527f1ae2bb464f19-a16ae7ed3ba4cd2e; tid=C147AEB095DC44D27D116088FDCFEBE9037B5214E238FB3812954513E7C1CDBB8BFCEF41053520F8E2514812DCAA714146BA8577047FD40FC663F7DED577815C1322AA34D58F19089C9F237F47BB73B738C2CC3CA4AB5380FF5CED13324B50BD1D919882B6498BC836D4610DAA37C6281C6A18D4E98054921E3B29FB37198308E7894ADA347424819EBB4EC84162469E7FE397BC7F683B2BA9350877C73A99446D492E139A23847D18C071029B68A428; clientType=10; accountType=5"
    }

    response = requests.post(url, headers=headers)
    print(response.json())
    data = response.json()
    data = data['data'][0]
    lists = data['list']

    try:
        os.mkdir('Assets/img/{0}'.format(user_id))
    except:
        pass


    for list in lists:
        print(list['goods_name'])
        download_image(list['bg_image'], user_id, 'image1.jpg')
        download_image(list['goods_pic'], user_id, 'image2.jpg')

        # 打开图片
        img1 = Image.open('Assets/img/'+str(user_id)+'/image1.jpg')
        img2 = Image.open('Assets/img/'+str(user_id)+'/image2.jpg')

        # 调整第二张图片的宽度为200，保持长宽比不变
        height = 180
        width = int((img2.width * height) / img2.height)
        img2_resized = img2.resize((width, height))

        # 计算居中粘贴的位置
        x = (img1.width - img2_resized.width) // 2
        y = (img1.height - img2_resized.height) // 2

        # 创建一个新的空白图像，大小与第一张图片相同
        new_img = Image.new('RGB', img1.size)

        # 将第一张图片粘贴到新图像上
        new_img.paste(img1, (0, 0))

        # 将调整后的第二张图片居中粘贴到新图像上
        new_img.paste(img2_resized, (x, y), mask=img2_resized.convert('RGBA'))

        draw = ImageDraw.Draw(new_img)
        font = ImageFont.truetype("Assets/fontFamily.ttf", 36)

        text = list['goods_name']
        text_position = (36, new_img.height-50)
        text_color = (255, 255, 255)  # 白色
        draw.text(text_position, text, fill=text_color, font=font)

        text = list['rmb_price']
        text_position = (new_img.width-136, new_img.height-50)
        text_color = (255, 255, 255)  # 白色
        draw.text(text_position, text, fill=text_color, font=font)


        # 保存新图像
        new_img.save('Assets/img/'+str(user_id)+'/'+list['goods_id']+'.jpg')

        # 删除旧图片
        os.remove('Assets/img/'+str(user_id)+'/image1.jpg')
        os.remove('Assets/img/'+str(user_id)+'/image2.jpg')

    #将Assets/img/'+str(user_id)+'/‘下的所有图片上下堆叠合并
    # 图片文件夹路径
    folder_path = f"Assets/img/{user_id}/"

    # 获取文件夹中所有图片文件
    image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    # 创建一个列表来存储所有图片
    images = []
    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        img = Image.open(image_path)
        images.append(img)

    # 获取所有图片的尺寸
    widths, heights = zip(*(i.size for i in images))

    # 计算合并后的图片宽度和高度
    max_width = max(widths)
    total_height = sum(heights) + (len(images)-1)*20

    # 创建一个新的空白图像，用于存储合并后的图像
    merged_image = Image.new('RGB', (max_width, total_height), color='white')

    # 将所有图片堆叠到一起
    y_offset = 0
    for img in images:
        merged_image.paste(img, (0, y_offset))
        y_offset += img.size[1] + 20

    # 保存合并后的图像
    merged_image.save(f"Assets/img/{user_id}/merged.jpg")

    #得到这张合并后图片的base64
    with open(f'Assets/img/{user_id}/merged.jpg', 'rb') as f:
        base64_data = base64.b64encode(f.read())
        base64_data = base64_data.decode('utf-8')

    shutil.rmtree('Assets/img/' + str(user_id))
    return base64_data
    # return [list['goods_id'] for list in lists]


# 将该图像转为base64存入all_pic_base64中

if __name__ == '__main__':
    pic = get_shop(1342171891)
