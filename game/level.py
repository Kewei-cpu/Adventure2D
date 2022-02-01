import time

from game.block import *
from game.constants import *
from game.item import *
from game.resources import filepath


class LevelEngine:
    def __init__(self):
        self.blocks = pygame.sprite.Group()

        self.width = int(WINWIDTH / BLOCK_W)
        self.height = int(WINHEIGHT / BLOCK_H)

        self.levelStructure = [[None for i in range(self.height)] for i in range(self.width)]

        # player
        self.blocksAroundPlayer = []

        # level time
        self.levelTimeStart = time.time()
        self.levelTime = 0

    def generateLevel(self, num):

        levelTxt = filepath(f'level{num}.txt')
        self.levelStructure = [[None for i in range(self.height)] for i in range(self.width)]

        with open(levelTxt, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f.readlines()):
                for j, letter in enumerate(line):
                    if letter == '#':
                        self.levelStructure[j][i] = BlockSprite(j, i)
                    elif letter == '@':
                        self.plyerStartX = j
                        self.plyerStartY = i
                    elif letter == '*':
                        self.levelStructure[j][i] = FinishItem(j, i)
                    elif letter == '%':
                        self.levelStructure[j][i] = DeadItem(j, i)

        self.levelTimeStart = time.time()


level = LevelEngine()
