import scrapy
import unicodedata


class QuotesSpider(scrapy.Spider):

    name = "quotes"
    first_url = 'https://www.fortinos.ca'
    start_urls = [
        first_url + '/search/page/~item/chicken/~sort/recommended/~selected/true',
    ]

    
    def parse(self, response):
        j = 0
        res = (response.css('div.product-name-wrapper').css('a::attr(href)').extract())
        for i in response.css('div.item'):
            next_page = res[j]
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parseTwo)
            j=j+1

    def parseTwo(self, response):
        for i in response.css('div.main-nutrition-attr'):
            label = (i.css('span.nutrition-label::text').extract())[0].encode('utf-8').strip('\n\t')
            amount = (i.css('div.main-nutrition-attr::text').extract())[1].encode('utf-8').strip('\n\t')
            unit = amount.split(' ')[1]
            amount = amount.split(' ')[0]
            print label + ": " + amount + " " + unit
