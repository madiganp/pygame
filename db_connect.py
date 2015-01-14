__author__ = 'madiganp'

import mysql.connector
from mysql.connector import errorcode

print("Connecting to pygamescores database...")
usr = raw_input("Username: ")

cnx = mysql.connector.connect(user=usr, password="jfkd", host='localhost', database='pygamescores')
print("Closing the connection...")
cnx.close()