# -*- coding: utf-8 -*-
import scrapy
from ..items import *
from ..SqliteOperator import *
import time
import sys
import urllib

conn = sqlite3.connect('tencentURL')
table = 'tencentURL'
fields = ('URL','Time')
db_create_table(conn, table, fields, ('URL'))
conn.text_factory=str
kw = sys.argv[2]
gQuery = None

class YoukuSpider(scrapy.Spider): ##re bo
    name = 'qq'
    allowed_domains = ['qq.com']

    def __init__(self,query):
        self.cnt = 0
        self.nameCnt = 1
        self.suffix = time.strftime('%Y-%m-%d-%H-%M-%S-', time.localtime(time.time()))
        self.start_urls = []
        gQuery = query

        for i in range(1,21):
            self.start_urls.append('https://v.qq.com/x/search/?q=' + query + '&cur=' + str(i) + '&filter=sort=1')

        print(urllib.quote(query))


    def parse(self, response):
        item = TencentkeywordItem()
        for each in response.xpath('.//div[@class="result_item result_item_h _quickopen"]'):
            link = each.xpath('./a/@href').extract()[0]
            # title = each.xpath('./strong[@class="figure_title figure_title_two_row"]/a[@title]/text()').extract()[0]
            item['link']=link.encode('utf-8')

            if db_table_get_count(conn, table, ('URL=?', [str(item['link'])])) == 0:
                self.cnt += 1
                if self.cnt % 100 == 0:
                    self.nameCnt += 1

                with open('Tencenturl ' + str(self.suffix) + str(self.nameCnt) + '.txt', 'a')as f:
                    rows = [fields]
                    curTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    rows.append((str(item['link']), curTime))
                    db_table_add_rows(conn, table, rows, ['URL'])
                    f.write(str(item['link']) + '\n')

            # yield item
        # yield scrapy.Request(url=self.urls[self.cnt],callback =self.parse)
        # self.cnt += 1
