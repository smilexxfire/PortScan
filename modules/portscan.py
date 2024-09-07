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

        # 开启扫描
        if self.task["module_name"] == "nmap":
            mynmap.run(self.task["ip"], self.task["port"])
        elif self.task["module_name"] == "naabu":
            naabu.run(self.task["ip"], self.task["port"])
        logger.log('INFOR', f'Finished port scan of {self.task["ip"]}')


if __name__ == '__main__':
    portscan = PortScan({"ip": "192.168.1.1", "port": "1-22000", "module_name": "nmap"})
    portscan.run()