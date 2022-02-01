import pygame
import time

from game.block import BlockSprite
from game.item import ItemSprite
from game.constants import *
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

        # level score

    def generateLevel(self, num):

        levelTxt = filepath(f'level{num}.txt')

        with open(levelTxt, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f.readlines()):
                for j, letter in enumerate(line):
                    if letter == '#':
                        self.levelStructure[j][i] = BlockSprite(j, i)
                    elif letter == '@':
                        self.plyerStartX = j
                        self.plyerStartY = i
                    elif letter == '*':
                        self.levelStructure[j][i] = ItemSprite(j, i)


        self.levelTimeStart = time.time()


level = LevelEngine()
