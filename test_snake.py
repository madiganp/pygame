from unittest import TestCase
import unittest
from Snake import Snake
from db_connect import DBConnect
import random, pygame, sys


__author__ = 'madiganp'


class TestSnake(TestCase):
    global db, snake

    @classmethod
    def setUp(cls):
        pygame.init()
        db = DBConnect('pygamescores')
        snake = Snake(db)

    @classmethod
    def tearDown(cls):
        db.close_database


    # def test_showStartScreen(self):
    #     self.fail()
    #
    # def test_runGame(self):
    #     self.fail()
    #
    # def test_drawScore(self):
    #     self.fail()
    #
    # def test_drawWorm(self):
    #     self.fail()
    #
    # def test_drawApple(self):
    #     self.fail()
    #
    # def test_drawGrid(self):
    #     self.fail()
    #
    # def test_drawPressKeyMsg(self):
    #     self.fail()
    #
    # def test_drawHighScores(self):
    #     self.fail()
    #
    # def test_checkForKeyPress(self):
    #     self.fail()

    def test_getRandomLocation(self):
        random_loc = snake.getRandomLocation()
        self.assertIsNotNone(random_loc)

    # def test_saveScore(self):
    #     self.fail()
    #
    # def test_showGameOverScreen(self):
    #     self.fail()
    #
    # def test_terminate(self):
    #     self.fail()


if __name__ == '__main__':
    unittest.main()