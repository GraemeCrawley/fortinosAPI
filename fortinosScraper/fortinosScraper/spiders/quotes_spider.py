import scrapy
import unicodedata
import urllib2
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import errorcode
from decimal import *
import string
import unicodedata


class QuotesSpider(scrapy.Spider): 


    cnx1 = mysql.connector.connect(user='root', password='Twelve-4', database='FORTINOS')

    cursor1 = cnx1.cursor(buffered=True)

    DB_NAME1 = 'FORTINOS'

    cursor1.execute("DROP database FORTINOS")
    cursor1.execute("CREATE database FORTINOS")


    TABLES = {}
    TABLES['foodInfo'] = (
        "CREATE TABLE `foodInfo` ("
        "  `ID` varchar(100) NOT NULL,"
        "  `brand` varchar(100) NOT NULL,"
        "  `name` varchar(100) NOT NULL,"
        "  `price` decimal(6,2) NOT NULL,"
        "  `proteinAmount` decimal(6,2) NOT NULL ,"
        "  `carbsAmount` decimal(6,2) NOT NULL ,"
        "  `fatAmount` decimal(6,2) NOT NULL ,"
        "  PRIMARY KEY (`ID`)"
        ") ENGINE=InnoDB;")


    try:
        cnx1.database = DB_NAME1 
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            cnx1.database = DB_NAME1
        else:
            print(err)
            exit(1)

    for name, ddl in TABLES.iteritems():
        try:
            print("Creating table {}: ".format(name))
            cursor1.execute(ddl)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

    searchItem = "chicken"

    
    name = "quotes"
    first_url = 'https://www.fortinos.ca'
    start_urls = [
        first_url + '/search/page/~item/chicken/~sort/recommended/~selected/true',
    ]

    cnx1.commit()

    cursor1.close()
    cnx1.close()
    


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


        cnx2 = mysql.connector.connect(user='root', password='Twelve-4', database='FORTINOS')

        cursor2 = cnx2.cursor(buffered=True)

        DB_NAME2 = 'FORTINOS'
        
        try:
            cnx2.database = DB_NAME2
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                create_database(cursor)
                cnx2.database = DB_NAME2
            else:
                print(err)
                exit(1)


        brand = response.css('div.row-product-name').css('span.product-sub-title::text').extract()[0]
        unicodedata.normalize('NFKD', brand).encode('ascii','ignore')
        brand = brand.strip(' \n\t')
        brand = brand.replace(u'\xa0','').encode('utf-8')
    

        try:
            name = response.css('div.row-product-name').css('h1.product-name::text').extract()[1].encode('utf-8').strip('\n\t')
        except IndexError:
            name = "NOT FOUND"  
        
        #PRICE IS GOOD TO GO
        try:
            firstPrice = response.css('span.reg-price-text::text').extract()[0].encode('utf-8').strip('\n\t')
            price = Decimal(firstPrice.split('$')[1])
        except IndexError:
            price = 0.00    
        
        #ID IS GOOD TO GO
        try:
            ID = (response.css('span.product-number').css('span.number::text')).extract()[0].encode('utf-8').strip('\n\t')
        except IndexError:
            ID = "NOT FOUND"
        
        amount = 0.00
        label = " "
        unit = " "
        carbsAmt = 0.00
        proteinAmt = 0.00
        fatAmt = 0.00

        for i in response.css('div.main-nutrition-attr'):
            label = (i.css('span.nutrition-label::text').extract())[0].encode('utf-8').strip('\n\t')
            amount = (i.css('div.main-nutrition-attr::text').extract())[1].encode('utf-8').strip('\n\t')
            unit = amount.split(' ')[1]
            amount = amount.split(' ')[0]
            if label == "Total Carbohydrate":
                carbsAmt = amount
            if label == "Protein":
                proteinAmt = amount
            if label == "Total Fat":
                fatAmt = amount

        data = {
          'ID': ID,
          'brand': brand,
          'name': name,
          'price': price,
          'proteinAmount': proteinAmt,
          'carbsAmount': carbsAmt,
          'fatAmount': fatAmt,
        }
        
        add_data = ("INSERT INTO foodInfo "
              "(ID, brand, name, price, proteinAmount, carbsAmount, fatAmount) "
              "VALUES (%(ID)s, %(brand)s, %(name)s, %(price)s, %(proteinAmount)s, %(carbsAmount)s, %(fatAmount)s)")

        
        cursor2.execute(add_data, data)
        

        cnx2.commit()

        cursor2.close()
        cnx2.close()
    def create_database(cursor):
            try:
                cursor.execute(
                    "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
            except mysql.connector.Error as err:
                print("Failed creating database: {}".format(err))
                exit(1)

