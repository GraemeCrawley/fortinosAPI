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


    cnx = mysql.connector.connect(user='root', password='Twelve-4', database='FORTINOS')

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
        "  `protein` varchar(100) NOT NULL ,"
        "  `proteinAmount` decimal(6,2) NOT NULL ,"
        "  `proteinUnit` varchar(100) NOT NULL ,"
        "  `carbs` varchar(100) NOT NULL ,"
        "  `carbsAmount` decimal(6,2) NOT NULL ,"
        "  `carbsUnit` varchar(100) NOT NULL ,"
        "  `fat` varchar(100) NOT NULL ,"
        "  `fatAmount` decimal(6,2) NOT NULL ,"
        "  `fatUnit` varchar(100) NOT NULL, "
        "  PRIMARY KEY (`ID`)"
        ") ENGINE=InnoDB")


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
            else:
                closeCursor
            j=j+1


    def parseTwo(self, response):
        
        brand = response.css('div.row-product-name').css('span.product-sub-title::text').extract()[0]
        unicodedata.normalize('NFKD', brand).encode('ascii','ignore')
        brand = brand.strip(' \n\t')
        brand = brand.replace(u'\xa0','').encode('utf-8')
    

        try:
            name = response.css('div.row-product-name::text').extract()[0].encode('utf-8').strip('\n\t')
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
            print ID
        except IndexError:
            ID = "NOT FOUND"
        
        amount = 0.00
        label = " "
        unit = " "
        carbs = " "
        carbsAmt = 0.00
        carbsUnit = " "
        protein = " "
        proteinAmt = 0.00
        proteinUnit = " "
        fat = " "
        fatAmt = 0.00
        fatUnit = " "

        for i in response.css('div.main-nutrition-attr'):
            label = (i.css('span.nutrition-label::text').extract())[0].encode('utf-8').strip('\n\t')
            amount = (i.css('div.main-nutrition-attr::text').extract())[1].encode('utf-8').strip('\n\t')
            unit = amount.split(' ')[1]
            amount = amount.split(' ')[0]
            if label == "Total Carbohydrate":
                carbs = label
                carbsAmt = amount
                carbsUnit = unit
            if label == "Protein":
                protein = label
                proteinAmt = amount
                proteinUnit = unit
            if label == "Total Fat":
                fat = label
                fatAmt = amount
                fatUnit = label

        data = {
          'ID': ID,
          'brand': brand,
          'name': name,
          'price': price,
          'protein': protein,
          'proteinAmount': proteinAmt,
          'proteinUnit': proteinUnit,
          'carbs': carbs,
          'carbsAmount': carbsAmt,
          'carbsUnit': carbsUnit,
          'fat': fat,
          'fatAmount': fatAmt,
          'fatUnit': fatUnit
        }
        print data
        
        add_data = ("INSERT INTO foodInfo "
              "(ID, brand, name, price, protein, proteinAmount, proteinUnit, carbs, carbsAmount, carbsUnit, fat, fatAmount, fatUnit) "
              "VALUES (%(ID)s, %(brand)s, %(name)s, %(price)s, %(protein)s, %(proteinAmount)s, %(proteinUnit)s, %(carbs)s, %(carbsAmount)s, %(carbsUnit)s, %(fat)s, %(fatAmount)s, %(fatUnit)s)")


        print "OKAY"
        self.cursor.execute(add_data, data)
        print "DONE"

       

    def create_database(cursor):
            try:
                cursor.execute(
                    "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
            except mysql.connector.Error as err:
                print("Failed creating database: {}".format(err))
                exit(1)

    def closeCursor():
        self.cnx.commit()

        self.cursor.close()
        self.cnx.close()

