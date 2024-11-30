<p align="center">
  <a href="https://www.pixiv.net/artworks/93066887">
    <img src="https://raw.githubusercontent.com/BlingCc233/go-cqhttp-ccbot/main/OtoAi.png" width="200" height="200" alt="Cc-bot">
  </a>
</p>

<div align="center">

# ValoBot

> 🤖一个基于<a href="https://github.com/NapNeko/NapCatQQ">NapCat</a>和<a href="https://github.com/pallets/flask">
> flask</a>的开箱即用的机器人

<p align="center">

  <a href="https://github.com/BlingCc233/ValoBot/releases">
    <img src="https://img.shields.io/github/v/release/BlingCc233/ValoBot?color=pink&include_prereleases&style=for-the-badge" alt="release">
  </a>

</p>

_ValoBot的动漫形象来源于[OhtoAi](https://wonder-egg-priority.com/character/ai/)_

</div>

## 声明

> [!NOTE]\
> 请勿用于非法用途


  <br/>

## 启动

- [Napcat](https://github.com/NapNeko/NapCatQQ)或[LLOneBot](https://github.com/LLOneBot/LLOneBot)请自行参考相关项目教程进行配置
- 无论你用哪种方式启动了插件，请确保你的服务器已开启`HTTP`服务，否则将无法接收到消息。且http监听端口应为`3000`
  ，上报地址建议为`http://localhost:3050`。
- 下载或克隆本仓库，并运行`pip install -r requirements.txt`安装依赖。（建议在python虚拟环境中运行）
- 修改`Config.py`中的`self_id`为机器人账号，`admin`为管理员帐号，同时将需要启用机器人的群号填入`group_white_list`中。
- 一般需要后台静默运行`OtherUse/`下的所有文件，由于基于flask，所以支持热重载，无需重启。
- 一些别的要求请查看`Plugins/`文件夹下的README.md
- 运行`bot_index.py`即可

## 功能

> 功能列表可以参考`api.py`里的`handle_msg`类

| 功能     | 说明                                          |
|--------|---------------------------------------------|
| 防撤回    | 管理员要向机器人私聊`recall 1/0`开关功能(默认关)             |
| 涩图bot  | 发送`/setu `或与涩图有关的关键句(参考[涩图](#涩图))           |
| 无畏契约商店 | 需要自行抓包掌瓦的某些字段才能使用                           |
| 今日人品   | 发送`/jrrp`或`/签到`获取今日运势                       |
| 点赞     | 发送`/赞我`机器人会为你点赞十次                           |
| 禁言     | admin账号可以发送`/禁言 @XX N`（N为分钟，0为取消禁言）禁言指定群成员  |
| 设精/取精  | 回复某条消息并包含`/设精` `/取精`可以设置/取消精华消息             |
| 答案之书   | 心里默想问题，发送`/答案`获得回答                          |
| 语言模型   | 接入了通义千问和`duck.ai`的gpt4o模型，有网络环境要求（@机器人可以对话） |
| AI语音回复 | 接入了`https://res.qpt.qq.com/qpilot` AI语音API  |
|        | 用`/echo_voice 文本`可以复读成语音消息                  |
| 文生图    | `/draw PROMPT`输入文本，即可生成图片(出图时间感人)           |
|        |                                             |

## 施工中的功能

- [ ] [狼人杀🐺](https://github.com/HUZHU-TEAM/Wolf-game "狼人杀")
- [ ] 打断+1复读
- [ ] QRcode二维码生成
- [X] AI文生图
- [ ] 进群欢迎 ~~验证~~
- [X] 群禁言
- [ ] 防闪照
- [ ] ~~超级管理员~~指定对象发送信息
- [X] 今日人品
- [ ] 数据库记录
- [ ] AES本地加密缓存

## 涩图

- 使用`/setu `自定义涩图类型，for instance:`/setu r18=1&tag=アロナ&num=2`
- <a href="https://api.lolicon.app/#/">参考涩图API调用方法</a>
- 也可以通过例如`给我来张涩图`，`给我来三张r18,ブルアカ涩图`, `整点涩图`，`看看ブルアカ涩图`请求涩图

## ！NOTICE ！

- 1.本机器人仅供学习交流使用，请勿用于非法用途，否则后果自负。
- 2.本机器人仍处于开发阶段，功能尚未完善，使用中的错误请反馈
- 3.机器人的部署需自行搭建，请自行Refer。
- 4.开源协议：General Public License v3.0
