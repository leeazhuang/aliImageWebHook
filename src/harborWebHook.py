# encoding=utf-8
import subprocess
from datetime import datetime

import requests
from flask import current_app


class webHookUtil:


    def push_image(self,post_json):

        try:
            imagesUrl = f"registry.{post_json['repository']['region']}.aliyuncs.com/{post_json['repository']['repo_full_name']}:{post_json['push_data']['tag']}"
            print(f"镜像名称：{imagesUrl}")
            image_name = post_json['repository']['name']
            # 要执行的命令
            result = self.execute_docker_command("docker pull "+imagesUrl)
            if result:
                print("镜像拉取成功")

            # 停止容器
            result = self.execute_docker_command("docker stop "+image_name)
            if result:
                print("容器停止成功")

            # 删除容器
            result = self.execute_docker_command("docker rm "+image_name)
            if result:
                print("容器删除成功")

            imageRun = f"docker run -p 8082:8082 --name {image_name} -v /data/{image_name}File/:/data/{image_name}File/  -d {imagesUrl}"
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # 容器启动
            result = self.execute_docker_command(imageRun)
            if result:
                print(f"容器:{imagesUrl}启动成功，时间：{current_time}")

            if result.returncode == 0:
                msg = f"发版成功  服务名称：{image_name}，镜像名称：{imagesUrl}"
            else:
                msg = f"发版失败  服务名称：{image_name}"
            requests.post(current_app.config['ROBOT_WEB_HOOK_URL'], json={
                'msgtype': 'text',
                'text': {
                    'content': msg
                }
            })

        except FileNotFoundError as e:
            print("file copy error:" + str(e))
            return False

    def execute_docker_command(self,cmd):
        try:
            # 执行命令，stdout和stderr重定向到PIPE
            result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # 检查命令执行结果
            if result.returncode != 0:
                raise subprocess.CalledProcessError(result.returncode, cmd)
            return result
        except subprocess.CalledProcessError as e:
            print(f"命令执行失败: {e.cmd}")
            return None