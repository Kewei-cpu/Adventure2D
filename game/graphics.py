import time

import pygame

from game.player import player
from game.level import level
from game.resources import filepath
from game.constants import *


class GraphicsEngine():
    def __init__(self, surface):
        self.screenSurface = surface

        # sprite groups
        self.allSprites = pygame.sprite.Group()
        #self.allSprites.add(level.blocks)
        self.allSprites.add(player)


        # load everything
        self.loadResources()

    def loadResources(self):
        # fonts
        self.scoreFont = pygame.font.Font(filepath('Minecraftia.ttf'), 16)


    def renderGame(self):
        self.screenSurface.fill((0, 0, 0))

        # draw blocks
        for x in range(int(WINWIDTH / BLOCK_W)):
            for y in range(int(WINHEIGHT / BLOCK_H)):
                block = level.levelStructure[x][y]
                if block is not None:
                    block.draw(self.screenSurface)

        # draw player
        #self.allSprites.draw(self.screenSurface)
        player.draw(self.screenSurface)

        # draw score

        self.drawTime()

    def drawTime(self):
        textSurface = self.scoreFont.render('TIME : ' + str(round(
            time.time() - level.levelTimeStart, 1)) + ' SECS', 0, (255, 255, 255))
        self.screenSurface.blit(textSurface, (20, 15))


