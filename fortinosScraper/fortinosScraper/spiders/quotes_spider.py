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

    searchItem = raw_input('Please enter your search term: ')
    pw = raw_input('Please enter your database password: ')

    cnx1 = mysql.connector.connect(user='root', password=pw, database='FORTINOS')

    cursor1 = cnx1.cursor(buffered=True)

    DB_NAME1 = 'FORTINOS'


    TABLES = {}
    TABLES[searchItem] = (
        "CREATE TABLE " + searchItem + " ("
        "  `ID` varchar(100) NOT NULL,"
        "  `brand` varchar(100) NOT NULL,"
        "  `name` varchar(100) NOT NULL,"
        "  `price` decimal(6,2) NOT NULL,"
        "  `proteinAmount` decimal(6,2) NOT NULL ,"
        "  `carbsAmount` decimal(6,2) NOT NULL ,"
        "  `fatAmount` decimal(6,2) NOT NULL ,"
        "  `PPG` decimal(6,2) ,"
        "  `foodTypeUpper` varchar(100) ,"
        "  `foodTypeLower` varchar(100) ,"
        "  PRIMARY KEY (`ID`)"
        ") ENGINE=InnoDB;")

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

    name = "quotes"
    first_url = 'https://www.fortinos.ca/'
    start_urls = [
        first_url + '/search/page/~item/' + searchItem + '/~sort/recommended/~selected/true',
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
            if err.errno == errorcode.ER_BAD_NOTDB_ERROR:
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
            name = 0.00
        
        #ID IS GOOD TO GO
        try:
            ID = (response.css('span.product-number').css('span.number::text')).extract()[0].encode('utf-8').strip('\n\t')
        except IndexError:
            ID = "NOT FOUND"

        

        try:
            PPG = response.css('div.qty').css('span.reg-qty::text').extract()[0].encode('utf-8').strip('\n\t')
            PPG = PPG.split('/')[0].split('$')[1]
        except IndexError:
            name = 0.00
        
        

        foodTypeUpper = self.normalize(response,4)
        foodTypeLower = self.normalize(response,5)
       
        
        amount = 0.00
        label = " "
        unit = " "
        carbsAmt = 0.00
        proteinAmt = 0.00
        fatAmt = 0.00

        for i in response.css('div.main-nutrition-attr'):
            label = (i.css('span.nutrition-label::text').extract())[0].encode('utf-8').strip('\n\t')
            amount = (i.css('div.main-nutrition-attr::text').extract())[1].encode('utf-8').strip('\n\t')
            try:
                unit = amount.split(' ')[1]
            except IndexError:
                try:
                    if type(amount.split(' ')[0]) == type("1"):
                        unit = amount.split(' ')[0]
                    else:
                        unit = "N/A"
                except IndexError:
                    unit = "N/A"
            amount = Decimal(amount.split(' ')[0])
            if label == "Total Carbohydrate":
                carbsAmt = Decimal(amount)
            if label == "Protein":
                proteinAmt = Decimal(amount)
            if label == "Total Fat":
                fatAmt = Decimal(amount)

        data = {
          'ID': ID,
          'brand': brand,
          'name': name,
          'price': price,
          'proteinAmount': proteinAmt,
          'carbsAmount': carbsAmt,
          'fatAmount': fatAmt,
          'PPG':PPG,
          'foodTypeUpper':foodTypeUpper,
          'foodTypeLower':foodTypeLower
        }
        
        add_data = ("INSERT INTO " + self.searchItem + " "
              "(ID, brand, name, price, proteinAmount, carbsAmount, fatAmount, PPG, foodTypeUpper, foodTypeLower) "
              "VALUES (%(ID)s, %(brand)s, %(name)s, %(price)s, %(proteinAmount)s, %(carbsAmount)s, %(fatAmount)s, %(PPG)s, %(foodTypeUpper)s, %(foodTypeLower)s)")

        
        cursor2.execute(add_data, data)

        cnx2.commit()
        cursor2.close()
        cnx2.close()

    def normalize(self, response,foodNum):
        foodType = str(response).split('/')[foodNum]
        if "%26" in foodType:
            foodType = foodType.replace("%26","&")
        if "%2C" in foodType:
            foodType = foodType.replace('%2C','')
        return foodType
            