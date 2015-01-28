import random, pygame, sys
from pygame.locals import *
import db_connect

def main():
    # Connect to the database to save the high scores
    db = db_connect.DB_Connect('pygamescores')
    pygame.init()
    snake = Snake()


class Snake:
    FPS = 15
    WINDOWWIDTH = 640
    WINDOWHEIGHT = 480
    CELLSIZE = 20
    assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
    assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
    CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
    CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)
    wormCoords = []

    #             R    G    B
    WHITE     = (255, 255, 255)
    BLACK     = (  0,   0,   0)
    RED       = (255,   0,   0)
    GREEN     = (  0, 255,   0)
    DARKGREEN = (  0, 155,   0)
    DARKGRAY  = ( 40,  40,  40)
    BGCOLOR = BLACK

    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'
    HEAD = 0 # Index of the worm's head

    def __init__(self):
        global FPSCLOCK, DISPLAYSURF, BASICFONT
        FPSCLOCK = pygame.time.Clock()
        DISPLAYSURF = pygame.display.set_mode((self.WINDOWWIDTH, self.WINDOWHEIGHT))
        BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
        pygame.display.set_caption('Snake')
        self.showStartScreen()
        while True:
            self.runGame()
            self.saveScore(len(self.wormCoords) - 3)
            self.showGameOverScreen()
            self.showHighScores()


    def showStartScreen(self):
        titleFont = pygame.font.Font('freesansbold.ttf', 100)
        titleSurf1 = titleFont.render('Snake!', True, self.WHITE, self.DARKGREEN)
        titleSurf2 = titleFont.render('Snake!', True, self.GREEN)

        degrees1 = 0
        degrees2 = 0

        pygame.event.get()  #clear out event queue

        while True:
            DISPLAYSURF.fill(self.BGCOLOR)
            rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
            rotatedRect1 = rotatedSurf1.get_rect()
            rotatedRect1.center = (self.WINDOWWIDTH / 2, self.WINDOWHEIGHT / 2)
            DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

            rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
            rotatedRect2 = rotatedSurf2.get_rect()
            rotatedRect2.center = (self.WINDOWWIDTH / 2, self.WINDOWHEIGHT / 2)
            DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

            self.drawPressKeyMsg()
            if self.checkForKeyPress():
                return
            pygame.display.update()
            FPSCLOCK.tick(self.FPS)
            degrees1 += 3 # rotate by 3 degrees each frame
            degrees2 += 7 # rotate by 7 degrees each frame


    def runGame(self):
        # Set a random start point.
        startx = random.randint(5, self.CELLWIDTH - 6)
        starty = random.randint(5, self.CELLHEIGHT - 6)
        self.wormCoords = [{'x': startx,     'y': starty},
                      {'x': startx - 1, 'y': starty},
                      {'x': startx - 2, 'y': starty}]
        direction = self.RIGHT

        # Start the apple in a random place.
        apple = self.getRandomLocation()

        while True: # main game loop
            for event in pygame.event.get(): # event handling loop
                if event.type == QUIT:
                    self.terminate()
                elif event.type == KEYDOWN:
                    if (event.key == K_LEFT or event.key == K_a) and direction != self.RIGHT:
                        direction = self.LEFT
                    elif (event.key == K_RIGHT or event.key == K_d) and direction != self.LEFT:
                        direction = self.RIGHT
                    elif (event.key == K_UP or event.key == K_w) and direction != self.DOWN:
                        direction = self.UP
                    elif (event.key == K_DOWN or event.key == K_s) and direction != self.UP:
                        direction = self.DOWN
                    elif event.key == K_ESCAPE:
                        self.terminate()

            # check if the worm has hit itself or the edge
            if self.wormCoords[self.HEAD]['x'] == -1 or self.wormCoords[self.HEAD]['x'] == self.CELLWIDTH or self.wormCoords[self.HEAD]['y'] == -1 or self.wormCoords[self.HEAD]['y'] == self.CELLHEIGHT:
                return # game over
            for wormBody in self.wormCoords[1:]:
                if wormBody['x'] == self.wormCoords[self.HEAD]['x'] and wormBody['y'] == self.wormCoords[self.HEAD]['y']:
                    return # game over

            # check if worm has eaten an apply
            if self.wormCoords[self.HEAD]['x'] == apple['x'] and self.wormCoords[self.HEAD]['y'] == apple['y']:
                # don't remove worm's tail segment
                apple = self.getRandomLocation() # set a new apple somewhere
            else:
                del self.wormCoords[-1] # remove worm's tail segment

            # move the worm by adding a segment in the direction it is moving
            if direction == self.UP:
                newHead = {'x': self.wormCoords[self.HEAD]['x'], 'y': self.wormCoords[self.HEAD]['y'] - 1}
            elif direction == self.DOWN:
                newHead = {'x': self.wormCoords[self.HEAD]['x'], 'y': self.wormCoords[self.HEAD]['y'] + 1}
            elif direction == self.LEFT:
                newHead = {'x': self.wormCoords[self.HEAD]['x'] - 1, 'y': self.wormCoords[self.HEAD]['y']}
            elif direction == self.RIGHT:
                newHead = {'x': self.wormCoords[self.HEAD]['x'] + 1, 'y': self.wormCoords[self.HEAD]['y']}
            self.wormCoords.insert(0, newHead)
            DISPLAYSURF.fill(self.BGCOLOR)
            self.drawGrid()
            self.drawWorm(self.wormCoords)
            self.drawApple(apple)
            self.drawScore(len(self.wormCoords) - 3)
            pygame.display.update()
            FPSCLOCK.tick(self.FPS)


    def drawScore(self, score):
        scoreSurf = BASICFONT.render('Score: %s' % (score), True, self.WHITE)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (self.WINDOWWIDTH - 120, 10)
        DISPLAYSURF.blit(scoreSurf, scoreRect)


    def drawWorm(self, wormCoords):
        for coord in wormCoords:
            x = coord['x'] * self.CELLSIZE
            y = coord['y'] * self.CELLSIZE
            wormSegmentRect = pygame.Rect(x, y, self.CELLSIZE, self.CELLSIZE)
            pygame.draw.rect(DISPLAYSURF, self.DARKGREEN, wormSegmentRect)
            wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, self.CELLSIZE - 8, self.CELLSIZE - 8)
            pygame.draw.rect(DISPLAYSURF, self.GREEN, wormInnerSegmentRect)


    def drawApple(self, coord):
        x = coord['x'] * self.CELLSIZE
        y = coord['y'] * self.CELLSIZE
        appleRect = pygame.Rect(x, y, self.CELLSIZE, self.CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, self.RED, appleRect)


    def drawGrid(self):
        for x in range(0, self.WINDOWWIDTH, self.CELLSIZE): # draw vertical lines
            pygame.draw.line(DISPLAYSURF, self.DARKGRAY, (x, 0), (x, self.WINDOWHEIGHT))
        for y in range(0, self.WINDOWHEIGHT, self.CELLSIZE): # draw horizontal lines
            pygame.draw.line(DISPLAYSURF, self.DARKGRAY, (0, y), (self.WINDOWWIDTH, y))


    def drawPressKeyMsg(self):
        pressKeySurf = BASICFONT.render('Press a key to play.', True, self.DARKGRAY)
        pressKeyRect = pressKeySurf.get_rect()
        pressKeyRect.topleft = (self.WINDOWWIDTH - 200, self.WINDOWHEIGHT - 30)
        DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


    def checkForKeyPress(self):
        for event in pygame.event.get():
            if event.type == QUIT:      #event is quit
                self.terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:   #event is escape key
                    self.terminate()
                else:
                    return event.key   #key found return with it
        # no quit or key events in queue so return None
        return None


    def getRandomLocation(self):
        return {'x': random.randint(0, self.CELLWIDTH - 1), 'y': random.randint(0, self.CELLHEIGHT - 1)}


    # Save the score in the database
    def saveScore(self, score):
        print 'Score: ', score
        db_connect.connect_to_database()




    def showGameOverScreen(self):
        gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
        gameSurf = gameOverFont.render('Game', True, self.WHITE)
        overSurf = gameOverFont.render('Over', True, self.WHITE)
        gameRect = gameSurf.get_rect()
        overRect = overSurf.get_rect()
        gameRect.midtop = (self.WINDOWWIDTH / 2, 10)
        overRect.midtop = (self.WINDOWWIDTH / 2, gameRect.height + 10 + 25)

        DISPLAYSURF.blit(gameSurf, gameRect)
        DISPLAYSURF.blit(overSurf, overRect)
        self.drawPressKeyMsg()
        pygame.display.update()
        pygame.time.wait(500)
        pygame.event.get()  #clear out event queue
        while True:
            if self.checkForKeyPress():
                return
            pygame.time.wait(100)


    def showHighScores(self):
        DISPLAYSURF.fill(self.BGCOLOR)
        highScoresFont = pygame.font.Font('freesansbold.ttf', 100)
        titleSurf = highScoresFont.render('High Scores', True, self.WHITE)
        titleRect = titleSurf.get_rect()
        titleRect.midtop = (self.WINDOWWIDTH / 2, 10)
        DISPLAYSURF.blit(titleSurf, titleRect)
        self.drawPressKeyMsg()
        pygame.display.update()
        pygame.time.wait(500)
        pygame.event.get()
        while True:
            if self.checkForKeyPress():
                DISPLAYSURF.fill(self.BGCOLOR)
                return
            pygame.time.wait(100)

    def terminate(self):
        pygame.quit()
        sys.exit()



if __name__ == '__main__':
    main()
