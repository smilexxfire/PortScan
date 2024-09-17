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
import uuid

from common.database.db import conn_db
from common.database.producer import RabbitMQProducer
QUEUE_NAME = "portscan"
class Producer(object):
    def __init__(self):
        pass
    def purge_queue(self, queue_name):
        '''
        清空指定队列

        :param queue_name: 队列名
        :return:
        '''
        producer = RabbitMQProducer(queue_name)
        producer.purge_queue()

    def send_task(self, task):
        uproducer = RabbitMQProducer(QUEUE_NAME)
        uproducer.publish_message(json.dumps(task))

    def produce_portscan_specified(self, ip: str, port: str, module: str):
        task = {
            "ip": ip,
            "port": port,
            "module_name": module,
            "task_id": str(uuid.uuid4())
        }
        self.send_task(task)

    def get_subdomains_from_domain(self, domain):
        db = conn_db("subdomain")
        subdomains = db.find({"domain": domain})
        subdomain_values = [doc.get("subdomain") for doc in subdomains]
        return subdomain_values
    def get_subdomains_from_assert(self, assert_name):
        db = conn_db("asserts")
        # 第一步：在 asserts 集合中根据 assert_name 查找所有文档
        assert_docs = db.find({"assert_name": assert_name})
        # 提取所有的 domain 字段
        domains = [doc.get("domain") for doc in assert_docs if doc.get("domain")]
        if not domains:
            return f"No documents found with assert_name: {assert_name} or no domain fields."
        db = conn_db("subdomain")
        # 第二步：在 subdomain 集合中查找所有与 domain 匹配的 subdomain
        subdomains = db.find({"domain": {"$in": domains}})
        # 提取 subdomain 值
        subdomain_values = [doc.get("subdomain") for doc in subdomains]
        return subdomain_values

    def get_ips_from_domain(self, domain):
        subdomains = self.get_subdomains_from_domain(domain)
        db = conn_db("dns_record")
        ips = db.find({"domain": {"$in": subdomains}})
        ips_values = [value for doc in ips for value in doc.get("a", [])]
        return list(set(ips_values))

    def get_ips_from_assert(self, assert_name):
        subdomains = self.get_subdomains_from_assert(assert_name)
        db = conn_db("dns_record")
        ips = db.find({"domain": {"$in": subdomains}})
        ips_values = [value for doc in ips for value in doc.get("a", [])]
        return list(set(ips_values))

    def produce_portscan_from_domain(self, domain:str, port:str, module:str):
        '''
        通过domain获取subdomain，subdomain获取ip，再对ip进行端口扫描

        :param domain:
        :param port:
        :param module:
        :return:
        '''
        ips = self.get_ips_from_domain(domain)
        # 针对每个ip发布任务
        for ip in ips:
            self.produce_portscan_specified(ip, port, module)
    def produce_portscan_from_assert(self, assert_name:str, port:str, module:str):
        '''
        通过资产定位所有相关ip，进行端口扫描

        :param assert_name:
        :param port:
        :param module:
        :return:
        '''
        ips = self.get_ips_from_assert(assert_name)
        for ip in ips:
            self.produce_portscan_specified(ip, port, module)

    def get_naabu_opened_ports(self, ip):
        db = conn_db("portscan_naabu")
        doc = db.find_one({"host": ip})
        return doc.get("open_ports") if doc else []

    def produce_portscan_from_domain_with_naabu(self, domain:str):
        '''
        从naabu获取扫描结果，将开放的端口给nmap做服务发现

        :param domain:
        :return:
        '''
        ips = self.get_ips_from_domain(domain)
        for ip in ips:
            opened_ports = self.get_naabu_opened_ports(ip)
            string_list = [str(num) for num in opened_ports]
            if len(string_list) > 0:
                self.produce_portscan_specified(ip, ",".join(string_list), "nmap")


if __name__ == '__main__':
    uproducer = Producer()
    uproducer.produce_portscan_specified("47.245.105.155", "top1000", "naabu")
    # producer.produce_portscan_specified("192.168.1.1", "80", "nmap")
    # producer.produce_portscan_from_domain("cee.edu.cn", "top1000", "naabu")
    # producer.produce_portscan_from_domain_with_naabu("cee.edu.cn")