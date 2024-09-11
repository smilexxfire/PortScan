"""
Module base class
"""

import time
import pymongo

from common.database.db import conn_db
from common.utils import delete_file_if_exists
from config import settings
from config.log import logger

class Module(object):
    def __init__(self, ip, port):
        self.results = list()  # 存放模块结果
        self.ip = ip
        self.port = port

        self.start = time.time()  # 模块开始执行时间
        self.end = None  # 模块结束执行时间
        self.elapse = None  # 模块执行耗时

        self.result_file = str(settings.result_save_dir.joinpath("result.temp.json"))
        self.set_execute_path()

    def begin(self):
        """
        begin log
        """
        logger.log('INFOR', f'Start {self.source} module')

    def get_targets(self, target: str = None, targets: list = None):
        if target is None and targets is None:
            return None
        result = []
        if target is not None:
            result.append(target)
        if targets is not None:
            result.extend(targets)
        return result

    def finish(self):
        """
        finish log
        """
        self.end = time.time()
        self.elapse = round(self.end - self.start, 1)
        logger.log('INFOR', f'Finished {self.source} module took {self.elapse} seconds find {len(self.open_ports)} opened ports'
                            f' of {self.ip}')

    def delete_temp(self):
        delete_file_if_exists(self.result_file)
        delete_file_if_exists(self.targets_file)

    def set_execute_path(self):
        if settings.PLATFORM == "Linux":
            self.execute_path = str(settings.third_party_dir.joinpath(self.source))
        elif settings.PLATFORM == "Windows":
            self.execute_path = str(settings.third_party_dir.joinpath(self.source + ".exe"))
    def save_targets(self):
        with open(self.targets_file, "w") as f:
            for domain in self.targets:
                f.write(domain.strip() + "\n")

    def save_db(self):
        """
        Save module results into the database
        """
        logger.log('INFOR', f'Start save db results')
        doc = self.results
        query = {"host": doc["host"]}
        while True:
            try:
                db = conn_db(self.collection)
                result = db.update_one(query, {"$set": doc}, upsert=True)
                # 获取操作结果并打印
                if result.matched_count > 0:
                    logger.log("INFOR", "Matched and Updated")
                    print(f"文档已更新: {result.matched_count}")
                elif result.upserted_id:
                    logger.log("INFOR", "Not matched and insert one")
                else:
                    logger.log("INFOR", "Not matched and not insert")
                return
            except Exception as e:
                logger.log("ERROR", f"error：{e}")
                logger.log("INFOR", "尝试重新save_db....")
