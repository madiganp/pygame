__author__ = 'madiganp'

import mysql.connector
from mysql.connector import errorcode

# Class that connects to a database
class DB_Connect:
    # The name of the database schema
    #DB_NAME = 'pygamescores'
    cnx = None
    cursor = None
    #cnx = mysql.connector.connect(user=usr, password="jfkd", host='localhost', database='pygamescores')


    TABLE = (
        "CREATE TABLE IF NOT EXISTS 'game_stats' ("
        "   'user' VARCHAR(64) NOT NULL,"
        "   'score' INT,"
        "   PRIMARY KEY ('user')"
        ") ENGINE=InnoDB"
    )

    def __init__(self, dbname):
        self.cnx = mysql.connector.connect(user="root")
        self.cursor = self.cnx.cursor()
        self.connect_to_db(dbname)

    # Attempt to connect to the database specified by
    # DB_NAME. If the database does not exist, create it.
    # Calls: create_database()
    def connect_to_db(self, dbname):
        try:
            self.cnx.database = dbname
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database " + dbname + " did not exits. Creating database.")
                self.create_database(self.cursor, dbname)
                self.cnx.database = dbname
            else:
                print(err)
                exit(1)


    # If the database specified in DB_NAME does not exist,
    # attempt to create a new instance of the database.
    def create_database(self, dbname):
        try:
            self.cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(dbname)
            )
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)


    def create_table(self):
        try:
            self.cursor.execute(self.TABLE)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("Table already exists.")
            else:
                print("Error creating highscores table.")
                print(err.msg)

    def save_score(self, score):
        topten = 0
        if score > topten:
            #save score
            score


    # Close the database.
    def close_database(self):
        print("Closing the connection...")
        if self.cnx is not None:
            self.cnx.close()
        else:
            print("Error closing connection (connection object is null.")




