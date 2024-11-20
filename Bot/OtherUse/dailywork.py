import schedule
import time
# from Bot.Plugins.jrrp import JRRP
import os

current_path = os.getcwd()

# 检查是否存在 "Assets" 文件夹
assets_folder = os.path.join(current_path, "Assets")
if not os.path.exists(assets_folder) or not os.path.isdir(assets_folder):
    # 切换到上级目录
    parent_path = os.path.dirname(current_path)
    os.chdir(parent_path)
def clean_job():
    os.remove('.jrrp.toml')

# 每天0点执行一次清空操作
schedule.every().day.at("00:00").do(clean_job)

if __name__ == "__main__":
    # 启动调度任务
    while True:
        schedule.run_pending()
        clean_job()
        time.sleep(1)
