阿里云新镜像通知

该项目为简单的devops脚本，用于接收阿里云镜像推送通知，并推送到企业微信。

收到推送后，会自动下载镜像，停止容器，删除容器，启动新容器。

启动新容器时可根据自己的需求，修改脚本。

若要做滚动更新，需要修改脚本中的滚动更新逻辑。