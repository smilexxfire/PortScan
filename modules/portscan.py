# -*- coding: UTF-8 -*-
'''
@Project ：PortScan 
@File    ：portscan.py
@IDE     ：PyCharm 
@Author  ：smilexxfire
@Email   : xxf.world@gmail.com
@Date    ：2024/9/5 20:50 
@Comment ： 
'''
from config.log import logger
from modules.myportscan import mynmap,naabu
from config import settings

class PortScan(object):

    def __init__(self, task: dict):
        self.task = task

    def run(self):
        logger.log('INFOR', f'Start port scan of {self.task["ip"]}')
        # 识别是否为默认端口
        if self.task["port"] == "top100":
            self.task["port"] = settings.top100
        elif self.task["port"] == "top1000":
            self.task["port"] = settings.top1000
        elif self.task["port"] == "full":
            self.task["port"] = settings.full

        ip = self.task["ip"]
        port = self.task["port"]
        task_id = self.task["task_id"]
        # 开启扫描
        if self.task["module_name"] == "nmap":
            mynmap.run(ip, port, task_id)
        elif self.task["module_name"] == "naabu":
            naabu.run(ip, port, task_id)
        else:
            logger.info("ERROR", f"module {self.task['module_name']} is not supported")
        logger.log('INFOR', f'Finished port scan of {ip}')


if __name__ == '__main__':
    portscan = PortScan({"ip": "192.168.1.1", "port": "1-22000", "module_name": "nmap", "task_id": "423131"})
    portscan.run()