# -*- coding: UTF-8 -*-
'''
@Project ：PortScan 
@File    ：producer.py
@IDE     ：PyCharm 
@Author  ：smilexxfire
@Email   : xxf.world@gmail.com
@Date    ：2024/9/5 19:33 
@Comment ： 
'''
import json
from common.database.producer import RabbitMQProducer
from config.settings import RABBITMQ_QUEUE_NAME

def purge_queue(queue_name):
    """
    清空队列

    :param queue_name: 队列名称
    :return:
    """
    producer = RabbitMQProducer(queue_name)
    producer.purge_queue()

def send_task(task):
    producer = RabbitMQProducer(RABBITMQ_QUEUE_NAME)
    producer.publish_message(json.dumps(task))

def portscan_producer_specified(ip:str, port:str, module:str):
    task = {
        "ip": ip,
        "port": port,
        "module_name": module
    }
    send_task(task)

if __name__ == '__main__':
    portscan_producer_specified("192.168.1.1", "1-20000", "nmap")
