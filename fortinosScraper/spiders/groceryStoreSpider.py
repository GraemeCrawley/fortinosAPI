import scrapy
import unicodedata
import mysql.connector
import string
import unicodedata
import re
from mysql.connector import errorcode
from decimal import *
import getpass


# Main class for crawling
class GroceryStoreSpider(scrapy.Spider): 

    searchItem = raw_input('Please enter your search term: ')
    pw = getpass.getpass('Please enter your database password:')

    # Deal with spaces in search terms
    if len(searchItem.split(' ')) > 1:
	   tableName = "".join(searchItem.split(' '))
	   searchItem = "+".join(searchItem.split(' '))
    else:
        tableName = searchItem

    DB_NAME1 = 'FORTINOSSUGAR'
    cnx1 = mysql.connector.connect(user='root', password=pw, database=DB_NAME1)
    cursor1 = cnx1.cursor(buffered=True)
    searchPage = 2
    searchPageLimit = 276

    # Setup table with schema
    TABLES = {}
    TABLES[tableName] = (
        "CREATE TABLE " + tableName + " ("
        "  `ID` varchar(100) NOT NULL,"
        "  `brand` varchar(100) NOT NULL,"
        "  `name` varchar(100) NOT NULL,"
        "  `price` decimal(6,2) NOT NULL,"
        "  `PPG` decimal(6,2) ,"
        "  `prot` decimal(6,2) NOT NULL ,"
        "  `carb` decimal(6,2) NOT NULL ,"
        "  `fat` decimal(6,2) NOT NULL ,"
        "  `chol` decimal(6,2) NOT NULL ,"
        "  `sod` decimal(6,2) NOT NULL ,"
        "  `pota` decimal(6,2) NOT NULL ,"
        "  `satfat` decimal(6,2) NOT NULL ,"
        "  `transfat` decimal(6,2) NOT NULL ,"
        "  `polyfat` decimal(6,2) NOT NULL ,"
        "  `omega` decimal(6,2) NOT NULL ,"
        "  `epa` decimal(6,2) NOT NULL ,"
        "  `dha` decimal(6,2) NOT NULL ,"
        "  `monofat` decimal(6,2) NOT NULL ,"
        "  `dietfiber` decimal(6,2) NOT NULL ,"
        "  `sugars` decimal(6,2) NOT NULL ,"
        "  `othercarb` decimal(6,2) NOT NULL ,"
        "  `foodTypeUpper` varchar(100) ,"
        "  `foodTypeLower` varchar(100) ,"
        "  PRIMARY KEY (`ID`)"
        ") ENGINE=InnoDB;")

    # Use schema to create table
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

    # Setup url
    name = "grocery"
    first_url = 'https://www.fortinos.ca/'
    start_urls = [first_url + 'search/showMoreProducts/~item/'+ searchItem + '/~sort/recommended/~selected/true?json=true&itemsLoadedonPage=48']


    cnx1.commit()
    cursor1.close()
    cnx1.close()
    

    # First parse level, used for search page
    def parse(self, response):  
        j = 0
        res = (response.css('div.product-name-wrapper').css('a::attr(href)').extract())
        # Loop through each item
        for i in response.css('div.item'):
            next_page = res[j]
            if next_page is not None:
                next_page = response.urljoin(next_page)
                # Call parseInfo to parse the info page
                yield scrapy.Request(next_page, callback=self.parseInfo)
            j=j+1
        print "SEARCH PAGE: " + str(self.searchPage)
        print "PAGE LIMIT " + str(self.searchPageLimit)
        # Check to see if we've reached the end of the page
        if self.searchPage < self.searchPageLimit:
                    next_page = response.url.split('fortinos.ca')[1].split('itemsLoadedonPage')[0] + "itemsLoadedonPage=" + str(self.searchPage*48)
                    self.searchPage+=1
                    next_page = response.urljoin(next_page)
                    yield scrapy.Request(next_page, callback=self.parse)


    # Second parse level, used for information page
    def parseInfo(self, response):


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
        satfat = 0.00
        transfat = 0.00
        polyfat = 0.00
        omega = 0.00
        epa = 0.00
        dha = 0.00
        monofat = 0.00
        dietfiber = 0.00
        sugars = 0.00
        othercarb = 0.00
        a = None
        b = None
        c = None
        for i in response.css('div.first'):
            label = ""
            amount = 0.00
            subLabel = ""
            subAmount = 0.00
           
            try:
                label = i.css('span.nutrition-label::text').extract()[0].encode('utf-8').strip('\n\t')
                amount = (i.css('div.first::text').extract())[1].encode('utf-8').strip('\n\t')    
            except IndexError:
                continue
    
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
                carb = amount
            if label == "Protein":
                prot = amount
            if label == "Total Fat":
                fat = amount
            if label == "Cholesterol":
                chol = amount
            if label == "Sodium":
                sod = amount
            if label == "Potassium":
                pota = amount
            if label == "Saturated Fat":
                satfat = amount
            if label == "Trans. Fat":
                transfat = amount
            if label == "Polyunsaturated Fat":
                polyfat = amount
            if label == "Omega":
                omega = amount
            if label == "EPA":
                epa = amount
            if label == "DHA":
                dha = amount
            if label == "Monounsaturated Fat":
                monofat = amount
            if label == "Dietary Fiber":
                dietfiber = amount
            if label == "Sugars":
                sugars = amount
            if label == "Other Carbohydrate":
                othercarb = amount




        data = {
          'ID': ID,
          'brand': brand,
          'name': name,
          'price': price,
          'PPG':PPG,
          'prot': prot,
          'carb': carb,
          'fat': fat,
          'chol': chol,
          'sod':sod,
          'pota': pota,
          'satfat': satfat,
          'transfat': transfat,
          'polyfat': polyfat,
          'omega': omega,
          'epa': epa,
          'dha': dha,
          'monofat': monofat,
          'dietfiber': dietfiber,
          'sugars':sugars,
          'othercarb': othercarb,
          'foodTypeUpper':foodTypeUpper,
          'foodTypeLower':foodTypeLower
        }

        add_data = ("INSERT INTO " + self.tableName + " "
              "(ID, brand, name, price, PPG, prot, carb, fat, chol, sod, pota, satfat, transfat, polyfat, omega, epa, dha, monofat, dietfiber, sugars, othercarb, foodTypeUpper, foodTypeLower) "
              "VALUES (%(ID)s, %(brand)s, %(name)s, %(price)s, %(PPG)s, %(prot)s, %(carb)s, %(fat)s, %(chol)s, %(sod)s, %(pota)s, %(satfat)s, %(transfat)s, %(polyfat)s, %(omega)s, %(epa)s, %(dha)s, %(monofat)s, %(dietfiber)s, %(sugars)s, %(othercarb)s, %(foodTypeUpper)s, %(foodTypeLower)s)")

        
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
