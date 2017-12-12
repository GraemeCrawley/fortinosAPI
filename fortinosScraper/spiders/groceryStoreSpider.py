import scrapy
import unicodedata
import urllib2
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import errorcode
from decimal import *
import string
import unicodedata
import re


class GroceryStoreSpider(scrapy.Spider): 

    searchItem = raw_input('Please enter your search term: ')
    pw = raw_input('Please enter your database password: ')
    if len(searchItem.split(' ')) > 1:
	   tableName = "".join(searchItem.split(' '))
	   searchItem = "+".join(searchItem.split(' '))
    else:
        tableName = searchItem

    DB_NAME1 = 'FORTINOS'

    cnx1 = mysql.connector.connect(user='root', password=pw, database=DB_NAME1)

    cursor1 = cnx1.cursor(buffered=True)

    
    searchPage = 2
<<<<<<< HEAD
    searchPageLimit = 50
=======
    searchPageLimit = 4
>>>>>>> cc49340... created optimization model for nutrition based on lowest cost/100g. Results of a couple of tests are in 'subproblems' file. Done for tonight.

    TABLES = {}
    TABLES[tableName] = (
        "CREATE TABLE " + tableName + " ("
        "  `ID` varchar(100) NOT NULL,"
        "  `brand` varchar(100) NOT NULL,"
        "  `name` varchar(100) NOT NULL,"
        "  `price` decimal(6,2) NOT NULL,"
        "  `prot` decimal(6,2) NOT NULL ,"
        "  `carb` decimal(6,2) NOT NULL ,"
        "  `fat` decimal(6,2) NOT NULL ,"
        "  `chol` decimal(6,2) NOT NULL ,"
        "  `sod` decimal(6,2) NOT NULL ,"
        "  `pota` decimal(6,2) NOT NULL ,"
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

    name = "grocery"
    first_url = 'https://www.fortinos.ca/'
    start_urls = [first_url + 'search/showMoreProducts/~item/'+ searchItem + '/~sort/recommended/~selected/true?json=true&itemsLoadedonPage=48']

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
        print "SEARCH PAGE: " + str(self.searchPage)
        print "PAGE LIMIT " + str(self.searchPageLimit)
        if self.searchPage < self.searchPageLimit:
                    next_page = response.url.split('fortinos.ca')[1].split('itemsLoadedonPage')[0] + "itemsLoadedonPage=" + str(self.searchPage+1)
                    self.searchPage+=1
                    next_page = response.urljoin(next_page)
                    yield scrapy.Request(next_page, callback=self.parse)


    def parseTwo(self, response):


        cnx2 = mysql.connector.connect(user='root', password=self.pw, database=self.DB_NAME1)

        cursor2 = cnx2.cursor(buffered=True)

        DB_NAME2 = self.DB_NAME1
        
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
    
        #ID IS GOOD TO GO
        try:
            ID = (response.css('span.product-number').css('span.number::text')).extract()[0].encode('utf-8').strip('\n\t')
        except IndexError:
            ID = "NOT FOUND"

        
    
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
        
        

        

   
        PPG = response.css('div.qty').css('span.reg-qty::text').extract()[0].encode('utf-8').strip('\n\t')
        if len(PPG.split('/')) < 2:
            PPG = 0.00
        else:
            a = PPG.split('/')[1]
            if(a  == "g" or a == " g" or a == "G" or a == " G"):
                PPG = Decimal((float(PPG.split('/')[0].split('$')[1].split('\xc2\xa0')[0]))*100)
            if(a  == "l" or a == " l" or a  == "L" or a == " L"):
                PPG = Decimal((float(PPG.split('/')[0].split('$')[1].split('\xc2\xa0')[0]))/1000)
            
            else:
                PPG = Decimal(PPG.split('/')[0].split('$')[1].split('\xc2\xa0')[0])

        
        
        

        foodTypeUpper = self.normalize(response,4)
        foodTypeLower = self.normalize(response,5)
       
        
        amount = 0.00
        label = " "
        unit = " "
        carb = 0.00
        prot = 0.00
        fat = 0.00
        qnty = None
        chol = 0.00
        pota = 0.00
        sod = 0.00
        a = None
        b = None
        c = None
        for i in response.css('div.main-nutrition-attr'):
            label = (i.css('span.nutrition-label::text').extract())[0].encode('utf-8').strip('\n\t')
            amount = (i.css('div.main-nutrition-attr::text').extract())[1].encode('utf-8').strip('\n\t')
            qnty = (response.css('span.nutrition-summary-value::text').extract())[0].encode('utf-8')
            a = qnty
            amountMeasurement = ""

            #Get serving size
            if re.search('(.*?[g,G,m,M])',qnty) is not None:
                qnty = re.search('([\d.,\d]\d+ ?[g,G,m,M])',qnty)
                b = qnty
                qnty = re.search('\d+',qnty.group(0))
                c = qnty
                qnty = float(qnty.group(0))
            else:
                qnty = re.search('\d+',qnty)
                qnty = float(qnty.group(0))

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

            amountMeasurement = str(amount.split(' ')[1])
            amount = Decimal((float(amount.split(' ')[0]))/qnty*100)
            if amountMeasurement == "MG" or amountMeasurement == "mg" or amountMeasurement == "Mg" or amountMeasurement == "mG":
                amountMeasurement = "g"
                amount = amount / 1000
            if label == "Total Carbohydrate":
                #print "amnt4: " + label + ": " + str(amount) + " " + amountMeasurement
                carb = amount
            if label == "Protein":
                #print "amnt5: " + label + ": " + str(amount) + " " + amountMeasurement
                prot = amount
            if label == "Total Fat":
                #print "amnt6: " + label + ": " + str(amount) + " " + amountMeasurement
                fat = amount
            if label == "Cholesterol":
                #print "amnt7: " + label + ": " + str(amount) + " " + amountMeasurement
                chol = amount
            if label == "Sodium":
                #print "amnt7: " + label + ": " + str(amount) + " " + amountMeasurement
                sod = amount
            if label == "Potassium":
                #print "amnt7: " + label + ": " + str(amount) + " " + amountMeasurement
                pota = amount




        data = {
          'ID': ID,
          'brand': brand,
          'name': name,
          'price': price,
          'prot': prot,
          'carb': carb,
          'fat': fat,
          'chol': chol,
          'sod':sod,
          'pota': pota,
          'PPG':PPG,
          'foodTypeUpper':foodTypeUpper,
          'foodTypeLower':foodTypeLower
        }

        add_data = ("INSERT INTO " + self.tableName + " "
              "(ID, brand, name, price, prot, carb, fat, chol, sod, pota, PPG, foodTypeUpper, foodTypeLower) "
              "VALUES (%(ID)s, %(brand)s, %(name)s, %(price)s, %(prot)s, %(carb)s, %(fat)s, %(chol)s, %(sod)s, %(pota)s, %(PPG)s, %(foodTypeUpper)s, %(foodTypeLower)s)")

        
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

    def conversion(amount, measurement):
        print o
            
