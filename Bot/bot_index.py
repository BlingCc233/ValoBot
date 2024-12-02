from flask import Flask, request, jsonify
import api
import logging

from Config import debug_mode
from Config import client_port

if debug_mode:
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)

@app.route("/", methods=['POST'])
def root():
    data = request.json  # 获取事件数据

    if debug_mode:
        logging.info(data)

    api.handle(data)
    return jsonify({})

if __name__ == "__main__":
    print(debug_mode)
    app.run(port=client_port, debug=debug_mode)
