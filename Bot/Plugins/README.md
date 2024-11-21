# 用前必看

## 这里是目前已有的插件的注意事项

### 无畏契约商店
无畏契约每日商店功能需要自行抓包掌瓦的`app.mval.qq.com`请求头中`Cookie`的`userId`和`tid`
  并以下面的格式新建`valo_config.py`填入其中

```python
user_data = {
    QQ号: {
        'userId': '',
        'tid': ''
    }
}
# 多个QQ号请用`,`创建字典
```

### 语言模型
LLM需要一个`llm_config.py`文件，内容如下：
```python
api_key = 'hf-XXXXXXXXXXXX'
```
要求你填入自己的hugging face的[api key](https://huggingface.co/docs/hub/security-tokens)，用于调用hugging face的模型。

## 网络环境要求

- 国内服务器无法直接访问hugging face的模型，需要代理
- 个人推荐使用[v2rayA](https://github.com/v2rayA/v2rayA)
- 按照[这里](https://v2raya.org/docs/prologue/installation/debian/)的教程配置好v2rayA，可以使用自己的订阅，有国外VPS的也可使用[v2ray安装脚本](https://github.com/233boy/v2ray/wiki/V2Ray%E4%B8%80%E9%94%AE%E5%AE%89%E8%A3%85%E8%84%9A%E6%9C%AC)搭建一个跳板（记得开放相应端口）