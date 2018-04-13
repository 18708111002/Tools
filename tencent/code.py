#--*coding=utf-8*--
import urllib2
from lxml import etree
from bs4 import BeautifulSoup
import json
import time

def loadpage(begin,end,url):
    for page in range(begin,end+1):
        print("page: " + str(page))
        url = url+str(page)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
        request = urllib2.Request(url,headers=headers)
        response = urllib2.urlopen(request)
        html = response.read()
        dealpage(html)
def dealpage(html):
    # soup = BeautifulSoup(html,'lxml')
    Html = etree.HTML(html)
    items = {}
    video_list = Html.xpath('.//li[@class = "list_item"]')
    # time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    for each in video_list:
        link = each.xpath('./a[@class = "figure"]/@href')[0]
        title = each.xpath('./strong[@class="figure_title figure_title_two_row"]/a[@title]/text()')[0]
        items['link'] = link.encode('utf-8')
        items['title'] = title.encode('utf-8')
        writepage(items)

def writepage(items):
    with open("url.txt", 'a') as f:
        f.write(items['link'] + "\n")

import sys

def main():

    beginpage = int(sys.argv[1])
    endpage = int(sys.argv[2])
    url = sys.argv[3]
    output = sys.argv[4]

    loadpage(beginpage,endpage,url)


if __name__=="__main__":
    main()
