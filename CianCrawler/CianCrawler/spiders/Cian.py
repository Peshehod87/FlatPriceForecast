# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
#from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request
from CianCrawler.items import FlatItem

class CianSpider(CrawlSpider):
    name = 'Cian'
    allowed_domains = ['https://www.cian.ru']
    start_urls = ['https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&region=1&p=3']
    #rules = (
    # The following rule is for pagination
    #Rule(SgmlLinkExtractor(allow=(r'\?p=\d+$'),), follow=True))

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, cookies={'serp_view_mode':'table'}, callback=self.parse)

    def parse(self, response):
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
            yield item