import unicodedata
import urllib2
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import errorcode
from decimal import *
import string
import unicodedata


def create_database(cursor):
    try:
        cursor.execute(
        	"DROP DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
        cursor.execute(    
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed with database: {}".format(err))
        exit(1)


DB_NAME = raw_input('Please enter your database to reset: ')
pw = raw_input('Please enter your password: ')

cnx = mysql.connector.connect(user='root', password=pw, database='FORTINOS')

cursor = cnx.cursor(buffered=True)



try:
        cnx.database = DB_NAME 
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)

cnx.commit()

cursor.close()
cnx.close()


