import requests

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
    "Cookie": "openid=A0D4E7CC8A838994E0B3E0949950AF90; access_token=2CE6F344548A0720E60ACF41EF50799C; appid=102061775; acctype=qc; userId=JA-527f1ae2bb464f19-a16ae7ed3ba4cd2e; tid=C147AEB095DC44D27D116088FDCFEBE9037B5214E238FB3812954513E7C1CDBB8BFCEF41053520F8E2514812DCAA714146BA8577047FD40FC663F7DED577815C1322AA34D58F19089C9F237F47BB73B738C2CC3CA4AB5380FF5CED13324B50BD1D919882B6498BC836D4610DAA37C6281C6A18D4E98054921E3B29FB37198308E7894ADA347424819EBB4EC84162469E7FE397BC7F683B2BA9350877C73A99446D492E139A23847D18C071029B68A428; clientType=10; accountType=5"
}

data = {
    "scene": "v3_sJUHrAIELSAJyy_xkojaUby8J8yA6ivM1BRXnqjhK5oBlj0fq_p2B7i0RdXQ4iHaP-5F_dgzlgzTDYuyO1XRQWlyUGWA5R9txtuIEvEJpvy2JnMG6_HDvFKYpF--JD7wXSbe9JNnrNukN4cguIYGYJVsbWlQNmyuGzgK1LXuhBxz92UCxaaomwA0ohai7eKs7645KttrHI6ZuEOQ5_iGgQ=="
}

response = requests.post(url, headers=headers, json=data)

print(response.status_code)
print(response.text)
