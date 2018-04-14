# -*- coding: utf-8 -*-

import sys

sys.path.append('..')

# 参考相对引用，百度 python import机制
from ..items import *
class QqSpider(scrapy.Spider): ##zuixinshangjia
    name = 'qq'
    allowed_domains = ['qq.com']
    url = 'http://v.qq.com/x/list/ent?&offset='

    start_urls = []
    for i in range(0,991):
        start_urls.append('http://v.qq.com/x/list/ent?&offset='+str(i) + '&sort=40')
    def parse(self, response):
        item = CrawltencentItem()
        for each in response.xpath('.//li[@class = "list_item"]'):
            link = each.xpath('./a[@class = "figure"]/@href').extract()[0]
            # title = each.xpath('./strong[@class="figure_title figure_title_two_row"]/a[@title]/text()').extract()[0]
            item['link']=link.encode('utf-8')
            # item['title']=title.encode('utf-8')
            yield item
        # if self.offset<990:
        #     self.offset+=30
        # yield scrapy.Request(url=self.url+str(self.offset),callback =self.parse)
