import unittest
from unittest import TestCase

from Snake import Snake
from db_connect import DBConnect


__author__ = 'madiganp'

class TestSnake(TestCase):

    # Integration Test: Test the connection to the database and assert that
    # the database 'pygamescores' exists.
    def test_connect_to_db(self):
        db = DBConnect()
        self.assertTrue(db.connect_to_db('pygamescores'))
        db.close_database()

    # Functional Test: Assert that the high scores persist.
    def test_persistence(self):
        db1 = DBConnect()
        db1.connect_to_db('pygamescores')
        snake = Snake(db1, True, True)
        snake.saveScore(db1, 100, False)
        db1.close_database()

        db2 = DBConnect()
        db2.connect_to_db('pygamescores')
        highscores2 = db2.getScores()
        self.assertTrue(highscores2[0][1] == 100)

    #
    # def test_snake(self):
    #     self.fail()


    # Assert that the Snake's terminate function works.
    def test_terminate_snake(self):
        with self.assertRaises(SystemExit):
            snake = Snake(None, True, True)
            snake.terminate()

if __name__ == '__main__':
    unittest.main()