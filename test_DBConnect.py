import unittest
from unittest import TestCase
from db_connect import DBConnect

__author__ = 'madiganp'

class TestDBConnect(TestCase):

    def test_connect_to_db(self):
        db = DBConnect()

        #self.assertFalse(db.connect_to_db('should_return_false'))
        self.assertTrue(db.connect_to_db('pygamescores'))

        db.close_database()

    # def test_create_database(self):
    #     self.fail()
    #
    # def test_create_table(self):
    #     self.fail()
    #
    # def test_save_score(self):
    #     self.fail()
    #
    # def test_close_database(self):
    #     self.fail()

if __name__ == '__main__':
    unittest.main()