# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from .settings import REDIS_PORT, REDIS_HOST, MODE, MONGODB_HOST, MONGODB_PORT, MONGODB_PASSWORD, MONGODB_USER
import redis as r

LOCAL = "127.0.0.1"


class LagouPipeline(object):
    def __init__(self):
        self.client = r.Redis(REDIS_HOST if MODE != 'LOCAL' else LOCAL, port=REDIS_PORT)
        self.conn = MongoClient(MONGODB_HOST if MODE != 'LOCAL' else LOCAL, MONGODB_PORT)
        self.conn.admin.authenticate(MONGODB_USER, MONGODB_PASSWORD)
        self.mongo = self.conn.Lagou.Lagou

    def process_item(self, item, spider):
        self.mongo.insert_one(dict(item))
        return item
