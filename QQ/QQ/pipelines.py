# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# class YoukuPipeline(object):
#     def process_item(self, item, YoukuSpider):
#         # content = json.dumps(dict(item),ensure_ascii=False)+'\n'
#         with open('youku.txt','a')as f:
#             f.write(str(item['link'])+'\n')
#         return item

class QqPipeline(object):
    def process_item(self, item, Spider):
        # content = json.dumps(dict(item),ensure_ascii=False)+'\n'
        with open('YOUKUEnturl.txt','a')as f:
            f.write(str(item['link'])+'\n')
        return item
