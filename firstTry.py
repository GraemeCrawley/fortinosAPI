# import libraries


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

searchItem = raw_input('Please enter your search term: ')

# specify the url
quote_page = 'https://www.fortinos.ca/search/page/~item/' + searchItem +'/~sort/recommended/~selected/true'

add_data = ("INSERT INTO foodInfo "
              "(ID, brand, name, price) "
              "VALUES (%(ID)s, %(brand)s, %(name)s, %(price)s)")

page = urllib2.urlopen(quote_page)

# parse the html using beautiful soap and store in variable `soup`
soup=BeautifulSoup(page,'html.parser')
# Take out the <div> of name and get its value

elements = soup.find_all('div', attrs={'class':'item'})

for i in elements:
	try:
		brand = i.find('span', attrs={'class':'js-product-entry-brand'}).text
	except AttributeError:
		brand = "NOT FOUND"	
	try:
		name = i.find('span', attrs={'class':'js-product-entry-name'}).text
	except AttributeError:
		name = "NOT FOUND"	
	try:
		firstPrice = i.find('span', attrs={'class':'reg-price-text'}).text
		price = Decimal(firstPrice.split('$')[1])
	except AttributeError:
		price = 0.00	
	try:
		ID = i.find('div', attrs={'class':'module-grocery-product quickview-simple clicked'}).get('data-product-id')
	except AttributeError:
		ID = "NOT FOUND"
	
	print brand + " " + name + " " + str(price) + " "
	print ID
	data = {
	  'ID': ID,
	  'brand': brand,
	  'name': name,
	  'price': price,
	}
	cursor.execute(add_data, data)




# Make sure data is committed to the database
cnx.commit()

cursor.close()
cnx.close()
