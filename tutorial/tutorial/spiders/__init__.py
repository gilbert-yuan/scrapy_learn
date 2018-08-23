# -*- coding: utf-8 -*-
import scrapy
import sys
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


class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance

driver = webdriver.Chrome()


class PhantomJSMiddleware(Singleton):
    def process_request(cls, request, callback=None):
        driver.get(request.url)
        time.sleep(1)
        old_sigle = ''
        click_doms = driver.find_element_by_xpath(
            "//li[@class='dropdown']/a/i[@class='fa fa-angle-down pointer fa-fw pagedown']")
        while driver.find_element_by_xpath("//a[@class='dropdown-toggle']/span[@class='pagination-text']").text != old_sigle:
            old_sigle = driver.find_element_by_xpath("//a[@class='dropdown-toggle']/span[@class='pagination-text']").text
            click_doms.click()
            time.sleep(0.5)
        data = driver.page_source.encode('utf-8')
        return HtmlResponse(driver.current_url, body=data, encoding='utf-8', request=request)


class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["odoo.net.cn"]
    start_urls = [
        "https://www.odoo.net.cn/categories",
    ]

    def parse(self, response):
        index = 0
        PhantomJS = PhantomJSMiddleware()
        for sel in response.xpath('//div/ul/li[contains(@class, "row clearfix")]'):
            item = TutorialItem()
            item['title'] = sel.xpath('//h2[contains(@class, "title")]/a/text()'
                                   )[index].extract().decode('utf-8').replace('\t', '').replace('\n', '')
            item['link'] = sel.xpath('//h2[contains(@class, "title")]/a/@href'
                                  )[index].extract().decode('utf-8').replace('\t', '').replace('\n', '')
            item['desc'] = sel.xpath('//div[contains(@class, "description")]/text()')[index].extract().decode('utf-8').replace('\t', '').replace('\n', '')
            index += 1
            if item['link']:
                #yield PhantomJS.process_request(Request('https://www.odoo.net.cn' + item['link']), callback=self.parse_item)
                Request('https://www.odoo.net.cn' + item['link'], callback=self.parse_item)
                yield Request('https://www.odoo.net.cn' + item['link'], callback=self.parse_item)

    def parse_item(self, response):
        index = 0
        test = response.xpath('//div/ul/li[contains(@class, "row clearfix category-item")]')
        for sel in response.xpath('//div/ul/li[contains(@class, "row clearfix category-item")]'):
            item = TutorialItem()
            item['title'] = sel.xpath('//h2[contains(@class, "title")]/a/text()'
                                      )[index].extract().decode('utf-8').replace('\t', '').replace('\n', '')
            item['link'] = sel.xpath('//h2[contains(@class, "title")]/a/@href'
                                     )[index].extract().decode('utf-8').replace('\t', '').replace('\n', '')
            index += 1
            yield item
            # if item['link']:
            #     yield Request(item['link'], callback=self.parse_item)
