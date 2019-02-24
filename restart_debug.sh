#!/usr/bin/env bash
# 本shell用于debug模式启动django项目
# 关闭原有服务
ps -ef|grep "runserver 0.0.0.0:8001"|grep -v grep|cut -c 10-15|xargs kill -9
# 切换到anaconda环境
source activate fapiao-api-deploy
# 更新代码
#git pull
# 前台启动django服务
python manage.py runserver 0.0.0.0:8001 --insecure