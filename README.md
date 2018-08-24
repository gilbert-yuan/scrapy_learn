# scrapy_learn
**scrapy_learn**
1. 闲来无事学爬虫，简单的爬虫以前写过，所以本次呢，就直接用框架了名为scrapy（可谓是python 爬虫届的翘楚）
2. 本着爬取的东西有用的目的就准备爬取 自己熟悉的odoo相关的网站  这个地址可谓是odoo论坛中的元老级的网站了，
	说爬就爬
    先安装 scrapy （不赘述，百度一下就都有了）
    然后就是初始化一个项目
    ```python
    scrapy crawl tutorial # dmo指的是项目名
    ```
   
    按照其他人推荐的教程先建几个简单的field
    ```python
    # -*- coding: utf-8 -*-
    # Define here the models for your scraped items
    #
    # See documentation in:
    # https://doc.scrapy.org/en/latest/topics/items.html
    import scrapy
    class TutorialItem(scrapy.Item):
        # define the fields for your item here like:
        title = scrapy.Field()
        link = scrapy.Field()
        desc = scrapy.Field()
    ```
    然后到spider 目录下新建一个py 记得加到__inti__.py 里面
    ```python
    # -*- coding: utf-8 -*-
    import scrapy
    import sys
    from scrapy.contrib.spiders import CrawlSpider, Rule
    from scrapy.contrib.linkextractors import LinkExtractor
    from selenium import webdriver
    import time
    from scrapy.http import HtmlResponse
    from tutorial.items import TutorialItem
    reload(sys)
    from selenium.webdriver.common.keys import Keys

    sys.setdefaultencoding("utf-8")
    from scrapy.http import Request
    class DmozSpider(scrapy.Spider):
        name = "dmoz"
        allowed_domains = ["odoo.net.cn"] # 这个是要爬的网站的域名
        start_urls = [
            "https://www.odoo.net.cn/categories", # 网站的初始的链接 不一定是根目录，有时候根目录不包含所有的链接
        ]
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip,deflate",
            "Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
            "Connection": "keep-alive",
            "Content-Type":" application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
            "Referer": "http://www.zhihu.com/"
            }
	    #rules = (  # 高级用法 ，暂时用不到 。
        #    Rule(SgmlLinkExtractor(allow = ('/question/\d+#.*?', )), callback = 'parse_page', follow = True), 
        #      Rule(SgmlLinkExtractor(allow = ('/question/\d+', )), callback = 'parse_page', follow = True),
        # )
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
                yield item
    ```
    上面提到 LinkExtractor , CrawlSpider, Rule 简单说一下我的理解，rule 是定义一定的规则提取初识页面的链接，传给callback用于对页面中匹配的url发起请求  ，callback 是访问链接后的处理数据的。可能也存在一些有用的数据
    
    
    
    
    
    
    
    
