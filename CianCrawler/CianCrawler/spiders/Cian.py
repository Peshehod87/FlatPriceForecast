# -*- coding: utf-8 -*-
import re
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
#from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request
from scrapy.contrib.loader import XPathItemLoader
from scrapy.linkextractors import LinkExtractor
from scrapy.contrib.loader.processor import Compose
from scrapy.contrib.loader.processor import MapCompose
from scrapy.contrib.loader.processor import TakeFirst

from CianCrawler.items import FlatItem

class FlatLoader(XPathItemLoader):
    default_input_processor = MapCompose(lambda s: re.sub('\s+', ' ', s.strip()))
    default_output_processor = TakeFirst()

class CianSpider(CrawlSpider):
    name = 'Cian'
    allowed_domains = ['www.cian.ru']
    start_urls = ['https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&region=1&sort=id_user&p=1']
    # The following rule is for pagination
    rules = (
        #Rule(LinkExtractor(restrict_xpaths="//a[@class='next_page']"), follow=True),
        Rule(LinkExtractor(allow=r"/cat\.php\?deal_type=sale&engine_version=2&offer_type=flat&p=\d+&region=1&sort=id_user"), callback='parse_item', follow= True),
        #Rule(LinkExtractor(), callback='parse_item'),
    )

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, cookies={'serp_view_mode':'table'}, callback=self.parse)

    def parse_item(self, response):
    #def parse(self, response):
        hxs = Selector(response)
        flatList = hxs.xpath('//table[@class="objects_items_list"]/tbody/tr[position()>1]')
        for flat in flatList:
            l = FlatLoader(FlatItem(), flat)
            l.add_xpath('address', '@address')
            l.add_xpath('underground', 'td[@class="objects_item_info_col_1"]//div[@class="objects_item_metro"]/a/text()')
            l.add_xpath('city', 'td[@class="objects_item_info_col_1"]//div[@class="objects_item_addr"][1]/a/text()')
            l.add_xpath('district', 'td[@class="objects_item_info_col_1"]//div[@class="objects_item_addr"][2]/a/text()')
            l.add_xpath('street', 'td[@class="objects_item_info_col_1"]//div[@class="objects_item_addr"][3]/a/text()')
            l.add_xpath('house', 'td[@class="objects_item_info_col_1"]//div[@class="objects_item_addr"][4]/a/text()')
            #should be parsed in two: remoteness and remotenessType
            l.add_xpath('remoteness', 'td[@class="objects_item_info_col_1"]//div[@class="objects_item_metro"]/span[@class="objects_item_metro_comment"]/text()')
            l.add_xpath('objectType', 'td[@class="objects_item_info_col_2"]/div/a/text()')
            #one field or three?
            #square = Field()
            l.add_xpath('squareTotal', 'td[@class="objects_item_info_col_3"]//table[@class="objects_item_props"]/tbody/tr/td/text()')
            l.add_xpath('price', 'td[@class="objects_item_info_col_4"]/div/div[@class="objects_item_price"]/strong/text()')
            l.add_xpath('floor', 'td[@class="objects_item_info_col_5"]/div[@class="objects_item_info_col_w"]/text()')
            l.add_xpath('description', 'td[@class="objects_item_info_col_9"]/div/div[@class="objects_item_info_col_comment_text no-truncate"]/text()')

            yield l.load_item()

    '''def parse(self, response):
        hxs = Selector(response)

        flatList = hxs.xpath('//table[@class="objects_items_list"]/tbody/tr[position()>1]')

        for flat in flatList:
            item = FlatItem()
            item['address'] = flat.xpath("@address").extract() #possible it should be AddressItem
            item['underground'] = flat.xpath('td[@class="objects_item_info_col_1"]//div[@class="objects_item_metro"]/a/text()').extract()
            item['city'] = flat.xpath('td[@class="objects_item_info_col_1"]//div[@class="objects_item_addr"][1]/a/text()').extract()
            item['district'] = flat.xpath('td[@class="objects_item_info_col_1"]//div[@class="objects_item_addr"][2]/a/text()').extract()
            item['street'] = flat.xpath('td[@class="objects_item_info_col_1"]//div[@class="objects_item_addr"][3]/a/text()').extract()
            item['house'] = flat.xpath('td[@class="objects_item_info_col_1"]//div[@class="objects_item_addr"][4]/a/text()').extract()
            #should be parsed in two: remoteness and remotenessType
            item['remoteness'] = flat.xpath('td[@class="objects_item_info_col_1"]//div[@class="objects_item_metro"]/span[@class="objects_item_metro_comment"]/text()').extract()
            item['objectType'] = flat.xpath('td[@class="objects_item_info_col_2"]/div/a/text()').extract()
            #one field or three?
            #square = Field()
            item['price'] = flat.xpath('td[@class="objects_item_info_col_4"]/div/div[@class="objects_item_price"]/strong/text()').extract()
            item['floor'] = flat.xpath('td[@class="objects_item_info_col_5"]/div[@class="objects_item_info_col_w"]/text()').extract()
            item['description'] = flat.xpath('td[@class="objects_item_info_col_9"]/div/div[@class="objects_item_info_col_comment_text no-truncate"]/text()').extract()
            #additionalInfo = Field()
            yield item'''