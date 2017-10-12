import unicodedata
import urllib2
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import errorcode
from decimal import *
import string
import unicodedata


DB_NAME = raw_input('Please enter your database to reset: ')
pw = raw_input('Please enter your password: ')

cnx = mysql.connector.connect(user='root', password=pw, database='FORTINOS')

cursor = cnx.cursor(buffered=True)

def create_database(cursor):
    try:
        cursor.execute(    
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
        print "Created database " + DB_NAME
    except mysql.connector.Error as err:
        print("Failed create database: {}".format(err))
        exit(1)

def drop_database(cursor):
    cursor.execute(
            "DROP DATABASE {}".format(DB_NAME))
    print "Dropped database " + DB_NAME

try:
        drop_database(cursor)
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


