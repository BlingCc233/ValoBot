import requests
import os
import subprocess

# 定义命令和密码
password = '0216'  # 替换为实际的密码
command = ['sudo', '-S', 'chmod', '777', '/Users/ccbling/Library/Containers/com.tencent.qq/Data/.config/QQ/NapCat/temp/']

# 使用 subprocess.run 执行命令，并传递密码
try:
    result = subprocess.run(command, input=password.encode(), check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("命令执行成功")
    print("输出:", result.stdout.decode('utf-8'))
except subprocess.CalledProcessError as e:
    print("命令执行失败")
    print("错误输出:", e.stderr.decode('utf-8'))

command = ['sudo', '-S', 'chmod', '777',
               '/Users/ccbling/PycharmProjects/ValoBot/Bot/Plugins/test/']

# 使用 subprocess.run 执行命令，并传递密码
try:
    result = subprocess.run(command, input=password.encode(), check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("命令执行成功")
    print("输出:", result.stdout.decode('utf-8'))
except subprocess.CalledProcessError as e:
    print("命令执行失败")
    print("错误输出:", e.stderr.decode('utf-8'))

import shutil

# 定义源文件路径和目标文件路径
source_file = '/Users/ccbling/PycharmProjects/ValoBot/Bot/Plugins/test/remind.mp3'
destination_file = '/Users/ccbling/Library/Containers/com.tencent.qq/Data/.config/QQ/NapCat/temp/6e7f7876-8604-4f2c-9ae8-72b3e1511d64.mp3'

# 使用 shutil.copyfile 复制文件
try:
    shutil.copyfile(source_file, destination_file)
    print("文件复制成功")
except FileNotFoundError as e:
    print(f"文件未找到: {e}")
except PermissionError as e:
    print(f"权限错误: {e}")
except Exception as e:
    print(f"发生错误: {e}")


response = requests.post('http://localhost:3000/send_group_msg', json={
    'group_id': 701436956,
    'message': [{
        'type': 'record',
        'data': {
            'file': 'file:///Users/ccbling/PycharmProjects/ValoBot/Bot/Plugins/test/remind.mp3'
        }
    }]
})

print(response.text)