# -*- coding: UTF-8 -*-
'''
@Project ：PortScan 
@File    ：portscan_worker.py
@IDE     ：PyCharm 
@Author  ：smilexxfire
@Email   : xxf.world@gmail.com
@Date    ：2024/9/5 23:49 
@Comment ： 
'''
import json
from common.database.consumer import RabbitMQConsumer
from modules.portscan import PortScan
from config.settings import RABBITMQ_QUEUE_NAME

class PortscanWorker(RabbitMQConsumer):

    def __init__(self):
        super().__init__(RABBITMQ_QUEUE_NAME)

    def task_handle(self):
        task = json.loads(self.message)
        subdomain = PortScan(task)
        subdomain.run()


if __name__ == '__main__':
    # 启动子域名扫描服务
    worker = PortscanWorker()
    worker.start_consuming()