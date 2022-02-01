import pygame

from game.block import BlockSprite
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
        self.speedup = False
        self.speeddown = False
        self.origJumpVel = 12.5
        self.jumpVel = self.origJumpVel
        self.gravity = 0.5

        # move speed
        self.moveSpeed = 4

        # targetting
        self.direction = DIR_RIGHT

        # score
        self.altitude = 0
        self.collectedResources = 0

    def calculateBlocksAroundPlayer(self):
        blocks = []
        plrX = (self.rect.x + 1) // BLOCK_W
        plrY = self.rect.y // BLOCK_H
        if isinstance(level.levelStructure[plrX][plrY + 1], BlockSprite):
            blocks.append(level.levelStructure[plrX][plrY + 1])  # below
        else:
            blocks.append(None)

        plrX1 = (self.rect.topright[0] - 1) // BLOCK_W
        plrY1 = self.rect.topright[1] // BLOCK_H

        if isinstance(level.levelStructure[plrX1][plrY + 1], BlockSprite):
            blocks.append(level.levelStructure[plrX1][plrY1 + 1])  # below
        else:
            blocks.append(None)

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
