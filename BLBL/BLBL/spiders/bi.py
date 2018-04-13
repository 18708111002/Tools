# -*- coding: utf-8 -*-
import scrapy
from BLBL.items import BlblItem

class BiSpider(scrapy.Spider):
    name = 'bi'
    allowed_domains = ['www.bilibili.com']
    url = 'https://www.bilibili.com/v/douga/mad/#/all/default/0/'
    offset = 1
    start_urls = [url+str(offset)]

    def parse(self, response):
        item = BlblItem()
        item_list = response.xpath('//div[@class="vd-list-cnt"]//div[@class="l-item"]').extract()
        print item_list
        for each in item_list:
            item['id']=each.xpath('./div[@class="l"]/div[@class="spread-module"]/a/@href').extract()[0]
            # print item['id']
            item['number']=each.xpath('.//div[@class="v-info"]/span[@class="v-info-i"]/span[1]/text()').extract()[0]
            yield item
        if self.offset<1093:
            self.offset+=1
        yield scrapy.Request(self.url+str(self.offset),callback=self.parse)



