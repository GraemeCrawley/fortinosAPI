import scrapy
import unicodedata
import urllib2
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import errorcode
from decimal import *



cnx = mysql.connector.connect(user='root', password='', database='FORTINOS')

cursor = cnx.cursor()

cursor.execute("DROP database FORTINOS")
cursor.execute("CREATE database FORTINOS")

DB_NAME = 'FORTINOS'



TABLES = {}
TABLES['foodInfo'] = (
    "CREATE TABLE `foodInfo` ("
    "  `ID` varchar(100) NOT NULL,"
    "  `brand` varchar(100) NOT NULL,"
    "  `name` varchar(100) NOT NULL,"
    "  `price` decimal(6,2) NOT NULL,"

    "  PRIMARY KEY (`ID`)"
    ") ENGINE=InnoDB")

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    cnx.database = DB_NAME  
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)

for name, ddl in TABLES.iteritems():
    try:
        print("Creating table {}: ".format(name))
        cursor.execute(ddl)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

searchItem = "chicken"


# specify the url
quote_page = 'https://www.fortinos.ca/search/page/~item/' + searchItem +'/~sort/recommended/~selected/true'

add_data = ("INSERT INTO foodInfo "
              "(ID, brand, name, price) "
              "VALUES (%(ID)s, %(brand)s, %(name)s, %(price)s)")




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

            try:
                brand = i.css('span.js-product-entry-brand::text')
            except AttributeError:
                brand = "NOT FOUND" 
            try:
                name = i.css('span.js-product-entry-name::text')
            except AttributeError:
                name = "NOT FOUND"  
            try:
                firstPrice = i.css('span.reg-price-text::text')
                price = Decimal(firstPrice.split('$')[1])
            except AttributeError:
                price = 0.00    
            
            #ID IS GOOD TO GO
            try:
                ID = (i.css('div.module-grocery-product::attr(data-product-id)')).extract()[0].encode('utf-8').strip('\n\t')
            except AttributeError:
                ID = "NOT FOUND"
            
            
            data = {
              'ID': ID,
              'brand': brand,
              'name': name,
              'price': price,
            }
            #cursor.execute(add_data, data)


            next_page = res[j]
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parseTwo)
            j=j+1
            break

    def parseTwo(self, response):
        for i in response.css('div.main-nutrition-attr'):
            label = (i.css('span.nutrition-label::text').extract())[0].encode('utf-8').strip('\n\t')
            amount = (i.css('div.main-nutrition-attr::text').extract())[1].encode('utf-8').strip('\n\t')
            unit = amount.split(' ')[1]
            amount = amount.split(' ')[0]
            print label + ": " + amount + " " + unit

cnx.commit()

cursor.close()
cnx.close()
