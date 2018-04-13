# -*- coding: utf-8 -*-
import scrapy
from QQ.items import *

# class QqSpider(scrapy.Spider): ##zuixinshangjia
#     name = 'qq'
#     allowed_domains = ['qq.com']
#     url = 'http://v.qq.com/x/list/ent?&offset='
#     offset = 0
#     start_urls = ['http://v.qq.com/x/list/ent?&offset='+str(offset) + '&sort=40']
#     def parse(self, response):
#         item = QqItem()
#         for each in response.xpath('.//li[@class = "list_item"]'):
#             link = each.xpath('./a[@class = "figure"]/@href').extract()[0]
#             # title = each.xpath('./strong[@class="figure_title figure_title_two_row"]/a[@title]/text()').extract()[0]
#             item['link']=link.encode('utf-8')
#             # item['title']=title.encode('utf-8')
#             yield item
#         if self.offset<990:
#             self.offset+=30
#         yield scrapy.Request(url=self.url+str(self.offset),callback =self.parse)

class QqSpider(scrapy.Spider): ##re bo
    name = 'youku'
    allowed_domains = ['youku.com']
    url = 'http://list.youku.com/category/video/c_86_d_1_s_1_p_' + '1'+ '.html'
    # offset = 1
    start_urls = ['http://list.youku.com/category/video/c_86_d_1_s_1_p_1.html',
                  'http://list.youku.com/category/video/c_86_d_1_s_2_p_1.html',
                  'http://list.youku.com/category/video/c_86_d_1_s_3_p_1.html',
                  'http://list.youku.com/category/video/c_86_d_1_s_4_p_1.html',
                  'http://list.youku.com/category/video/c_86_d_1_s_5_p_1.html'
                  ]
    cnt = 1
    urls =[]
    for i in range(2,26):
        urls.append('http://list.youku.com/category/video/c_86_d_1_s_1_p_' + str(i) + '.html')
        urls.append('http://list.youku.com/category/video/c_86_d_1_s_2_p_' + str(i) + '.html')
        urls.append('http://list.youku.com/category/video/c_86_d_1_s_3_p_' + str(i) + '.html')
        urls.append('http://list.youku.com/category/video/c_86_d_1_s_4_p_' + str(i) + '.html')
        urls.append('http://list.youku.com/category/video/c_86_d_1_s_5_p_' + str(i) + '.html')

    def parse(self, response):
        item = QqItem()
        for each in response.xpath('.//div[@class="p-thumb"]'):
            link = each.xpath('./a/@href').extract()[0]
            # title = each.xpath('./strong[@class="figure_title figure_title_two_row"]/a[@title]/text()').extract()[0]
            item['link']=link.encode('utf-8')

            yield item
        yield scrapy.Request(url=self.urls[self.cnt],callback =self.parse)
        self.cnt += 1