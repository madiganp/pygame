__author__ = 'madiganp'

import mysql.connector
from mysql.connector import errorcode

# The name of the database schema
DB_NAME = 'pygamescores'

# Create a table of game stats to add to the database.
TABLES = {}
TABLES['game_stats'] = (
    "CREATE TABLE IF NOT EXISTS 'game_stats' ("
    "   'user' VARCHAR(64) NOT NULL,"
    "   'score' INT,"
    "   PRIMARY KEY ('user')"
    ") ENGINE=InnoDB"
)

print("Connecting to database " + DB_NAME + "...")
usr = raw_input("Username: ")
cnx = mysql.connector.connect(user=usr)
cursor = cnx.cursor()

#cnx = mysql.connector.connect(user=usr, password="jfkd", host='localhost', database='pygamescores')

# If the database specified in DB_NAME does not exist,
# attempt to create a new instance of the database.
def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME)
        )
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

# Attempt to connect to the database specified by
# DB_NAME. If the database does not exist, create it.
# Calls: create_database()
def connect_to_database():
    try:
        cnx.database = DB_NAME
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database " + DB_NAME + " did not exits. Creating database.")
            create_database(cursor)
            cnx.database = DB_NAME
        else:
            print(err)
            exit(1)

# Close the database.
def close_database():
    print("Closing the connection...")
    cnx.close()





