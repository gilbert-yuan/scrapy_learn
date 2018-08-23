# -*- coding: utf-8 -*-
import scrapy
import sys
import os
from selenium import webdriver
import time
from scrapy.http import HtmlResponse
reload(sys)
sys.setdefaultencoding("utf-8")


class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance

chromedriver = "C:\Miniconda2\chromedriver\chromedriver.exe"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)

class PhantomJSMiddleware(Singleton):
    def process_request(cls, request, spider):
        driver.get(request.url)
        time.sleep(3)
        old_sigle = ''
        click_doms = driver.find_element_by_xpath(
            "//li[@class='dropdown']/a/i[@class='fa fa-angle-down pointer fa-fw pagedown']")
        while driver.find_element_by_xpath("//a[@class='dropdown-toggle']/span[@class='pagination-text']").text != old_sigle:
            old_sigle = driver.find_element_by_xpath("//a[@class='dropdown-toggle']/span[@class='pagination-text']").text
            click_doms.click()
            time.sleep(1)
        data = driver.page_source.encode('utf-8')
        return HtmlResponse(driver.current_url, body=data, encoding='utf-8', request=request)

