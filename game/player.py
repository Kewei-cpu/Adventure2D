import pygame

from game.constants import *
from game.level import level


class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([BLOCK_W - 4, BLOCK_H + 4])
        # make the player sprite a little taller than the blocks,
        # but NOT the rect
        self.image.fill(PLAYER_COLOR)

        self.rect = pygame.Rect((0, 0, BLOCK_W - 4, BLOCK_H))
        self.rect.x = 10
        self.rect.y = 250

        self.xVel = 0
        self.yVel = 0

        # jumping
        self.hollow = False
        self.hollow1 = False
        self.jumping = False
        self.onGround = False
        self.origJumpVel = 15
        self.jumpVel = self.origJumpVel
        self.gravity = 0.5

        # move speed
        self.moveSpeed = 2

        # targetting
        self.direction = DIR_RIGHT

        # score
        self.altitude = 0
        self.collectedResources = 0

    def calculateBlocksAroundPlayer(self):
        blocks = []
        plrX = self.rect.x // BLOCK_W
        plrY = self.rect.y // BLOCK_H

        blocks.append(level.levelStructure[plrX][plrY + 1])  # below

        plrX1 = self.rect.topright[0] // BLOCK_W
        plrY1 = self.rect.topright[1] // BLOCK_H

        blocks.append(level.levelStructure[plrX1][plrY1 + 1])  # below

        self.blocksAroundPlayer = blocks

    def draw(self, surface):
        y = self.rect.y + (self.rect.h - self.image.get_rect().h)
        surface.blit(self.image, (self.rect.x, y))


    def reset(self):
        self.rect.x = level.plyerStartX * BLOCK_W
        self.rect.y = level.plyerStartY * BLOCK_H

        self.xVel = 0
        self.yVel = 0
        self.direction = DIR_RIGHT


    def doJump(self):
        if self.jumping and not self.onGround:
            self.yVel = -self.jumpVel
            self.jumpVel -= self.gravity

        if self.onGround:
            self.jumping = False
            self.jumpVel = self.origJumpVel
            self.yVel = 0


# define player
player = PlayerSprite()
