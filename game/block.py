import pygame

from game.constants import *


class BlockSprite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.x = x
        self.y = y
        self.displayX = x * BLOCK_W
        self.displayY = y * BLOCK_H

        self.image = pygame.Surface([BLOCK_W, BLOCK_H])
        self.image.fill(BLOCK_COLOR)

        self.rect = self.image.get_rect()
        self.rect.x = self.displayX
        self.rect.y = self.displayY

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def __repr__(self):
        return f'BlockSprite({self.rect.x},{self.rect.y})'
