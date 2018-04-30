# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time
import sqlite3
from SqliteOperator import *

conn = sqlite3.connect('tencentURL')
table = 'tencentURL'
fields = ('URL','Time')
db_create_table(conn, table, fields, ('URL'))

conn.text_factory=str

class CrawltencentPipeline(object):
    def __init__(self):
        self.cnt = 0
        self.nameCnt = 1
        self.suffix = time.strftime('%Y-%m-%d-%H-%M-%S-', time.localtime(time.time()))

    def process_item(self, item, Spider):
        # content = json.dumps(dict(item),ensure_ascii=False)+'\n'
        if db_table_get_count(conn, table, ('URL=?', [str(item['link'])])) == 0:
            self.cnt += 1
            if self.cnt % 100 == 0:
                self.nameCnt += 1
            with open('Tencenturl ' + str(self.suffix) + str(self.nameCnt) +'.txt','a')as f:
                rows = [fields]
                curTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                rows.append((str(item['link']),curTime))
                db_table_add_rows(conn, table, rows, ['URL'])
                f.write(str(item['link'])+'\n')
        return item
