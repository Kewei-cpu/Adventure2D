import time

import pygame


from game.graphics import GraphicsEngine
from game.menus import *
from game.level import level
from game.block import BlockSprite
from game.item import *
from game.player import player



class GameEngine():
    def __init__(self, screenWidth, screenHeight):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight

        # screen
        self.screen = None

        # menu state
        self.GAME_STATE = MENU_MAIN

        # game
        self.clock = pygame.time.Clock()
        self.gameTime = time.time()
        self.gameRunning = True
        # self.currentLevel = 1

    def initializeGame(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            [self.screenWidth, self.screenHeight])
        pygame.display.set_caption('ADVENTURE 2')

        # engines
        self.graphicsEngine = GraphicsEngine(self.screen)

        # menus
        self.menuMain = MenuMain(self.screen, self)
        self.menuAbout = MenuAbout(self.screen, self)
        self.menuNext = MenuNext(self.screen, self)
        self.menuLoss = MenuLoss(self.screen, self)
        self.menuSelect = MenuSelect(self.screen, self)

        # start the loop
        self.gameLoop()

    def gameLoop(self):
        while self.gameRunning:

            if self.GAME_STATE == MENU_MAIN:
                self.menuMain.draw()
                self.menuMain.update()

            elif self.GAME_STATE == MENU_ABOUT:
                self.menuAbout.draw()
                self.menuAbout.update()

            elif self.GAME_STATE == MENU_SELECT:
                self.menuSelect.draw()
                self.menuSelect.update()

            elif self.GAME_STATE == MENU_LOSS:
                self.menuLoss.draw()
                self.menuLoss.update()

            elif self.GAME_STATE == MENU_NEXT:
                self.menuNext.draw()
                self.menuNext.update()

            elif self.GAME_STATE == MENU_INGAME:
                # handle input

                pygame.event.pump()
                for event in pygame.event.get():
                    self.handleInput(event)

                    if event.type == pygame.QUIT:
                        self.gameRunning = False
                        break

                # update everything
                self.playerMove()

                self.checkGameState()

                # draw everything
                self.graphicsEngine.renderGame()
                pygame.display.update()

                # limit fps
                self.clock.tick(60)


        # game not running any longer, so lets quit
        pygame.quit()

    def handleInput(self, event):
        global player
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.xVel = -player.moveSpeed
                player.direction = DIR_LEFT

            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.xVel = +player.moveSpeed
                player.direction = DIR_RIGHT

            # jump
            elif event.key == pygame.K_SPACE or event.key == pygame.K_w:
                if player.onGround:
                    player.jumping = True
                    player.onGround = False


            elif event.key == pygame.K_ESCAPE:
                self.GAME_STATE = MENU_SELECT

        elif event.type == pygame.QUIT:
            self.gameRunning = False

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.xVel += player.moveSpeed
                player.direction = DIR_LEFT

            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.xVel -= player.moveSpeed
                player.direction = DIR_RIGHT

    def setState(self, state):
        if state == MENU_INGAME:
            level.generateLevel(self.currentLevel)
            player.reset()


        self.GAME_STATE = state

    def checkGameState(self):
        for i in level.levelStructure:
            for j in i:
                if isinstance(j, FinishItem):
                    if pygame.sprite.collide_rect(player, j):
                        self.setState(MENU_NEXT)
                if isinstance(j, DeadItem):
                    if pygame.sprite.collide_rect(player, j):
                        self.setState(MENU_LOSS)

    def resetGame(self):
        self.currentLevel = 1
        self.currentScene = 0

        level.generateLevel()
        player.reset()

    def checkCollision(self, sprite, xVel, yVel):
        for x in range(len(level.levelStructure)):
            for y in range(len(level.levelStructure[x])):
                block = level.levelStructure[x][y]

                if isinstance(block, BlockSprite):
                    if pygame.sprite.collide_rect(sprite, block):
                        if xVel < 0:
                            sprite.rect.x = block.rect.x + block.rect.w
                        if xVel > 0:
                            sprite.rect.x = block.rect.x - sprite.rect.w

                        if yVel < 0:
                            sprite.rect.y = block.rect.y + block.rect.h
                            player.jumping = False
                            player.yVel = 0

                        if yVel > 0:
                            sprite.onGround = True
                            sprite.rect.y = block.rect.y - sprite.rect.h

    def playerMove(self):
        ''' this is done in GameEngine due to collision problems '''

        player.altitude = 15 - (player.rect.y + player.rect.h) // BLOCK_H

        if not player.onGround and not player.jumping:
            player.yVel += player.gravity
        player.doJump()
        player.calculateBlocksAroundPlayer()
        if player.onGround and not player.jumping:
            if not player.blocksAroundPlayer[0] and not player.blocksAroundPlayer[1] :
                player.hollow1 = player.hollow
                player.hollow = True

        if player.hollow1:
            player.onGround = False
            player.hollow = False
            player.hollow1 = False

        if player.xVel > player.moveSpeed:
            player.xVel = player.moveSpeed
        elif player.xVel < -player.moveSpeed:
            player.xVel = -player.moveSpeed

        if player.rect.x <= 0:
            player.rect.x = 0
        elif player.rect.x >= WINWIDTH - player.rect.w:
            player.rect.x = WINWIDTH - player.rect.w


        player.rect.x += player.xVel
        self.checkCollision(player, player.xVel, 0)
        player.rect.y += player.yVel
        self.checkCollision(player, 0, player.yVel)

        # move player and check collision
