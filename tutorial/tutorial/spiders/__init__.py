# -*- coding: utf-8 -*-
import scrapy
import sys
import os
from selenium import webdriver
import time
from scrapy.http import HtmlResponse
from tutorial.items import TutorialItem
reload(sys)
from selenium.webdriver.common.keys import Keys

sys.setdefaultencoding("utf-8")
from scrapy.http import Request

js = '''
    document.body.scrollTop +=1000;
    '''

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["odoo.net.cn"]
    start_urls = [
        "https://www.odoo.net.cn/categories",
    ]

    def parse(self, response):
        index = 0
        for sel in response.xpath('//div/ul/li[contains(@class, "row clearfix")]'):
            item = TutorialItem()
            item['title'] = sel.xpath('//h2[contains(@class, "title")]/a/text()'
                                   )[index].extract().decode('utf-8').replace('\t', '').replace('\n', '')
            item['link'] = sel.xpath('//h2[contains(@class, "title")]/a/@href'
                                  )[index].extract().decode('utf-8').replace('\t', '').replace('\n', '')
            item['desc'] = sel.xpath('//div[contains(@class, "description")]/text()')[index].extract().decode('utf-8').replace('\t', '').replace('\n', '')
            index += 1
            yield item
        for link in response.xpath('//h2[contains(@class, "title")]/a/@href').extract():
            yield Request('https://www.odoo.net.cn' + link.decode('utf-8').replace('\t', '').replace('\n', ''), callback=self.parse_item)
            break

    def parse_item(self, response):
        index = 0
        items = []
        for sel in response.xpath('//div/ul[contains(@class, "topic-list")]/li'):
            item = TutorialItem()
            if len(sel.xpath('//h2[contains(@class, "title")]/a/@href')) > index:
                item['title'] = sel.xpath('//h2[contains(@class, "title")]/a/text()')[index].extract().decode('utf-8').replace('\t', '').replace('\n', '')
            if len(sel.xpath('//h2[contains(@class, "title")]/a/@href')) > index:
                item['link'] = sel.xpath('//h2[contains(@class, "title")]/a/@href')[index].extract().decode('utf-8').replace('\t', '').replace('\n', '')
            index += 1
            items.append(item)
        return items
        # return True
