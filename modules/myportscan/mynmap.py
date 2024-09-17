# -*- coding: UTF-8 -*-
'''
@Project ：PortScan 
@File    ：nmap.py
@IDE     ：PyCharm 
@Author  ：smilexxfire
@Email   : xxf.world@gmail.com
@Date    ：2024/9/5 19:44 
@Comment ： 
'''
from common.module import Module
from common.task import Task
import nmap
from datetime import datetime


class Nmap(Module, Task):
    def __init__(self, ip: str, port: str, task_id: str):
        self.module = "portscan"
        self.source = "nmap"
        self.collection = "portscan_nmap"

        Module.__init__(self, ip, port)
        Task.__init__(self, task_id)

    def do_scan(self):
        self.nm = nmap.PortScanner()
        self.nm.scan(hosts=self.ip, ports=self.port, arguments="-Pn -sS -sV")

    def deal_data(self):
        # 处理扫描结果
        host = self.ip
        protocol = "tcp"
        self.open_ports = list()
        ports = self.nm[host][protocol].keys()
        for port in sorted(ports):
            state = self.nm[host][protocol][port].get('state', 'unknown')
            if not state == "open":
                continue
            service_info = self.nm[host][protocol][port]
            self.open_ports.append({
                "port": port,
                "service": service_info['name'],
                "product": service_info.get('product', 'N/A'),
                "version": service_info.get('version', 'N/A'),
                "extrainfo": service_info.get('extrainfo', 'N/A')
            })
        self.results = {
            "host": self.ip,
            "open_ports": self.open_ports,
            "insert_time": datetime.now()
        }

    def save_db(self):
        # print(self.results)
        if len(self.results["open_ports"]) > 0:
            super().save_db()

    def run(self):
        self.begin()
        self.receive_task()
        self.do_scan()
        self.deal_data()
        self.save_db()
        self.finish()
        self.finnish_task(self.elapse, len(self.open_ports))


def run(ip: str, port: str, task_id: str):
    unmap = Nmap(ip, port, task_id)
    unmap.run()


if __name__ == '__main__':
    run("192.168.1.1", "80", "123321-432432-43242")
