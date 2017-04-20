# -*- coding: utf-8 -*-
#from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.dupefilter import RFPDupeFilter
from scrapy.selector import HtmlXPathSelector
from searchEngine.items import SearchengineItem
class DmozSpider(CrawlSpider):
   name = "dmoz"
   allowed_domains = [
      "news.cn",
      "news.xinhuanet.com"
      ]
   start_urls = [
       "http://www.news.cn/",
       "http://www.news.cn/mil/index.htm",
       "http://www.news.cn/politics/"
       "http://www.news.cn/world/index.htm",
       "http://www.news.cn/tech/index.htm"
   ]
   rules = ( 
      #Rule(SgmlLinkExtractor(allow=('page/[0-9]+', ))),
      #Rule(SgmlLinkExtractor(allow=['/' ]),'item_parse')
      Rule(SgmlLinkExtractor(allow=('/', )),callback='item_parse'),
   )  
   def item_parse(self,response,dont_filter=False):
       #self.log("%s"%response.url)
      item = SearchengineItem()
      item['url'] = response.url
      item['title'] = response.selector.xpath('//title/text()').extract()
      item['keywords'] = response.selector.xpath('//meta[@name="keywords"]/@content').extract()
      item['description'] = response.selector.xpath('//meta[@name="description"]/@content').extract()
      for t in item['title']:
        print t.encode('utf-8')
      for t in item['keywords']:
        print t.encode('utf-8')
      for t in item['description']:
        print t.encode('utf-8')
      return item

      #print item['title']
'''
   def parse(self, response):
       #hxs = HtmlXPathSelector(response)
       #sites = hxs.select('//head')
       #res = HtmlXPathSelector(response)

      item = SearchengineItem()
       #for site in sites:
        #   item = SearchengineItem()
         #  item['title'] = site.select('//title/text()').extract()
          # item['link'] = site.select('meta/@keywords').extract()
           #item['desc'] = site.select('text()').extract()
           #items.append(item)
      item['title'] = response.selector.xpath('//title/text()').extract()
      item['keywords'] = response.selector.xpath('//meta[@name="keywords"]/@content').extract()
      item['description'] = response.selector.xpath('//meta[@name="description"]/@content').extract()
      for t in item['title']:
        print t.encode('utf-8')
      for t in item['keywords']:
        print t.encode('utf-8')
      for t in item['description']:
        print t.encode('utf-8')
      #print item['title']
      return item

'''
