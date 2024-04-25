# encoding: utf-8
import os
from flask import Flask,request
from src.harborWebHook import webHookUtil

app = Flask(__name__)
app.config['ROBOT_WEB_HOOK_URL'] = os.getenv('ROBOT_WEB_HOOK_URL', '<企业微信机器人url>')


@app.route('/imageup', methods=['POST'])
def push_image():
    post_json = request.get_json(force=True)
    print(f"收到阿里镜像推送事件:{post_json}")
    HookUtil = webHookUtil()
    HookUtil.push_image(post_json)
    return "ok"

    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
