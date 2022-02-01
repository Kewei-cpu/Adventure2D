import pygame
from game.constants import *


class ItemSprite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.displayX = x * BLOCK_W
        self.displayY = y * BLOCK_H

        self.image = pygame.Surface([BLOCK_W - 20, BLOCK_H - 20])
        self.image.fill(BLOCK_COLOR_FINISH)

        self.rect = self.image.get_rect()
        self.rect.x = self.displayX + (BLOCK_W - self.image.get_width())//2
        self.rect.y = self.displayY + (BLOCK_H - self.image.get_height())//2

    def draw(self, surface):
        surface.blit(self.image, self.rect)
