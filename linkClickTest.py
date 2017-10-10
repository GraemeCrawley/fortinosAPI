# -*- coding: utf-8 -*-
import scrapy


# item class included here 
class DmozItem(scrapy.Item):
    # define the fields for your item here like:
    link = scrapy.Field()
    attr = scrapy.Field()


class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["craigslist.org"]
    start_urls = [
    "http://chicago.craigslist.org/search/emd?"
    ]

    BASE_URL = 'http://chicago.craigslist.org/'

    def parse(self, response):
        links = response.xpath('//a[@class="hdrlnk"]/@href').extract()
        for link in links:
            absolute_url = self.BASE_URL + link
            yield scrapy.Request(absolute_url, callback=self.parse_attr)

    def parse_attr(self, response):
        item = DmozItem()
        item["link"] = response.url
        item["attr"] = "".join(response.xpath("//p[@class='attrgroup']//text()").extract())
        return item