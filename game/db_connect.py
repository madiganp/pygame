__author__ = 'madiganp'

import mysql.connector
from mysql.connector import errorcode

# Class that connects to a database
class DBConnect:
    global cnx, cursor     # The connection and cursor objects
    TABLE = (
        "CREATE TABLE IF NOT EXISTS `highscores` ("
        "   `user` VARCHAR(64) NOT NULL,"
        "   `score` INT NOT NULL"
        ") ENGINE=InnoDB"
    )

    # Constructor
    def __init__(self):
        self.cnx = mysql.connector.connect(user="root", password='jfkd', host='localhost')
        self.cnx.start_transaction(isolation_level='READ COMMITTED')
        self.cursor = self.cnx.cursor()


    # Attempt to connect to the database specified by
    # DB_NAME. If the database does not exist, create it.
    # Calls: create_database()
    def connect_to_db(self, db_name):
        try:
            self.cnx.database = db_name
            self.create_table()
            return True
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database '" + db_name + "' did not exist. Creating database.")
                self.create_database(db_name)
                self.cnx.database = db_name
                self.create_table()
                return False
            else:
                print(err)
                exit(1)


    # If the database specified in DB_NAME does not exist,
    # attempt to create a new instance of the database.
    def create_database(self, db_name):
        try:
            self.cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(db_name)
            )
            self.cnx.commit()   # Make sure data is committed to the database
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)


    # Function to create a table to hold the high scores.
    def create_table(self):
        try:
            self.cursor.execute(self.TABLE)
            self.cnx.commit()   # Make sure data is committed to the database
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("Table already exists.")
            else:
                print("Error creating high scores table.")
                print(err.msg)


    # If the user's score is within the top 10, save the name and score to the database.
    def save_score(self, username, new_score):
        # Check to see if the score is in the top ten:
        query = ("SELECT * FROM pygamescores.highscores ORDER BY score DESC LIMIT 10")
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        # If there are less than 10 accounts saved, automatically add it; otherwise must be greater than the 10th score.
        if (self.cursor.rowcount <= 9) or (new_score > rows[9][1]):
            #save score
            new_high = ("INSERT INTO highscores (user, score) VALUES (%s, %s)")
            data = (username, new_score)
            self.cursor.execute(new_high, data)
            self.cnx.commit()   # Make sure data is committed to the database

            self.cursor.execute(query)
            rows = self.cursor.fetchall()

        return rows


    # Close the database.
    def close_database(self):
        if self.cnx is not None:
            self.cnx.close()
        else:
            print("Error closing connection (connection object is null.")