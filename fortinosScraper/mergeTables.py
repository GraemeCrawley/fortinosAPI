import mysql.connector
from mysql.connector import errorcode
import sys


pw = raw_input('Please enter your database password: ')
	
cnx1 = mysql.connector.connect(user='root', password=pw, database='FORTINOS')

cursor1 = cnx1.cursor(buffered=True)

DB_NAME1 = 'FORTINOS'

val1 = 'beans'
val2 = 'beef'

a = ['soup', 'beans','beef','chicken','noodles','rice', 'lentils']
for i in a:
	print i
	val2 = i
	print val2
	cursor1.execute("INSERT IGNORE INTO " + val1 + " SELECT * FROM " + val2 + ";")


cnx1.commit()
cursor1.close()
cnx1.close()
