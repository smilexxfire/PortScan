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

QUEUE_NAME = "portscan"
class PortscanWorker(RabbitMQConsumer):

    def __init__(self):
        super().__init__(QUEUE_NAME)

    def task_handle(self):
        task = json.loads(self.message)
        portscan = PortScan(task)
        portscan.run()


if __name__ == '__main__':
    # 启动子域名扫描服务
    worker = PortscanWorker()
    worker.start_consuming()