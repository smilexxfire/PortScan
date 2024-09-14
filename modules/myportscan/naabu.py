# -*- coding: UTF-8 -*-
'''
@Project ：PortScan 
@File    ：naabu.py
@IDE     ：PyCharm 
@Author  ：smilexxfire
@Email   : xxf.world@gmail.com
@Date    ：2024/9/5 20:45 
@Comment ： 
'''
import datetime
import sys
import os
sys.path.append("D:\\pythonProject\\PortScan")

from common.module import Module
import subprocess

from config.log import logger
import json
class Naabu(Module):
    def __init__(self,ip:str,port:str):
        self.module = "portscan"
        self.source = "naabu"
        self.collection = "portscan_naabu"
        Module.__init__(self, ip, port)

    def do_scan(self):
        cmd = [self.execute_path, "-host", self.ip, "-Pn", "-p", self.port, "-j", "-o", self.result_file]
        subprocess.run(cmd)

    def deal_data(self):
        logger.log("INFOR", "Start deal data process")
        if not os.path.exists(self.result_file):
            return

        self.open_ports = list()
        with open(self.result_file, "r") as f:
            datas = f.readlines()
            json_list = [json.loads(data) for data in datas]
            for data in json_list:
                self.open_ports.append(data["port"])
        self.results = {
            "host": self.ip,
            "open_ports": self.open_ports,
            "insert_time": datetime.datetime.now()
        }
    def save_db(self):
        # print(self.results)
        if len(self.results["open_ports"]) > 0:
            super().save_db()

    def run(self):
        self.begin()
        self.do_scan()
        self.deal_data()
        self.save_db()
        self.finish()
def run(ip:str,port:str):
    naabu = Naabu(ip,port)
    naabu.run()

if __name__ == '__main__':
    run("192.168.1.1", "1-20000")