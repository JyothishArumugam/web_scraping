# -*- coding: utf-8 -*-
import scrapy
from bikes2.items import Bikes2Item
from scrapy.loader import ItemLoader


class HondaspySpider(scrapy.Spider):
    name = 'hondaspy'
    allowed_domains = ['bikewale.com']
    start_urls = ['https://www.bikewale.com/honda-bikes/']

    def parse(self, response):
        all_bikes = response.xpath("//*[@class='bikeDescWrapper']")
        for bike in all_bikes:
            next_url = bike.xpath('.//*[@class="modelurl"]/@href').extract_first()
            absolute_url = response.urljoin(next_url)
            yield scrapy.Request(url=absolute_url,callback=self.parse2)
    def parse2(self,sec_response):
        item = Bikes2Item()
        item['price'] = sec_response.xpath("//*[@id='new-bike-price']/text()").extract_first()
        item['name'] = sec_response.xpath('//*[@class="breadcrumb-link__label"]/text()').extract()[-1]

        yield item
