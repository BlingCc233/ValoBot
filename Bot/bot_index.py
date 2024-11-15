import uvicorn
from fastapi import FastAPI, Request
import api
import logging

from Config import debug_mode
if debug_mode:
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = FastAPI()


@app.post("/")
async def root(request: Request):
    data = await request.json()  # 获取事件数据
    api.handle(data)
    return {}

if __name__ == "__main__":
    print(debug_mode)
    uvicorn.run(app, port=8080)
