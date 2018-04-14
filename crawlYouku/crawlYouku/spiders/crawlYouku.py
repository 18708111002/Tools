# -*- coding: utf-8 -*-
import scrapy
from ..items import *

class YoukuSpider(scrapy.Spider): ##re bo
    name = 'youku'
    allowed_domains = ['youku.com']
    url = 'http://list.youku.com/category/video/c_86_d_1_s_1_p_' + '1'+ '.html'
    # offset = 1
    start_urls = []
    for i in range(1,26):
        for j in range(1,6):
            start_urls.append('http://list.youku.com/category/video/c_86_d_1_s_'+str(j)+'_p_' + str(i)+ '.html')


    def parse(self, response):
        item = CrawlyoukuItem()
        for each in response.xpath('.//div[@class="p-thumb"]'):
            link = each.xpath('./a/@href').extract()[0]
            # title = each.xpath('./strong[@class="figure_title figure_title_two_row"]/a[@title]/text()').extract()[0]
            item['link']=link.encode('utf-8')

            yield item
        # yield scrapy.Request(url=self.urls[self.cnt],callback =self.parse)
        # self.cnt += 1
