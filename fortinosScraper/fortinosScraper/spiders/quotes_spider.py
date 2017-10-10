import scrapy
import unicodedata


class QuotesSpider(scrapy.Spider):
    f = open('helloworld.txt','w')

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
            label = ((i.css('span.nutrition-label').extract_first()).encode('utf-8')).strip(' \t\n\r')
            amount = ((i.css('div.main-nutrition-attr').extract_first()).encode('utf-8')).strip(' \t\n\r')
            print label
            print type(label)
            print amount
            print type(amount)
