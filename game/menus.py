import pygame
import sys
from pygame.locals import *

from game.constants import *
from game.resources import filepath
from game.level import level


class MenuClass():
    def __init__(self, surface):
        '''menu object
        '''
        self.surface = surface

        self.backgroundColor = (0, 0, 0)

        self.titleFont = pygame.font.Font(filepath('Minecraftia.ttf'), 64)

        # menus
        self.selectedMenu = 0
        self.menus = []

        self.title = ''

        # keyboard events
        self.keyboardEvents = []

    def draw(self):
        self.surface.fill(self.backgroundColor)
        self.drawTitle()
        if len(self.menus):
            self.drawMenus()

        # update surface
        pygame.display.update()

    def drawTitle(self):
        title = self.titleFont.render(self.title, False, (255, 255, 255))
        rect = title.get_rect()
        objAmount = len(self.menus) + 1
        rect.centerx = WINWIDTH / 2
        rect.centery = WINHEIGHT / (objAmount + 1)
        self.surface.blit(title, rect)

    def drawMenus(self):
        for menu in self.menus:
            menu.draw(self.surface)

    def update(self):
        for event in pygame.event.get():
            self._handleEvents(event)

    def _handleEvents(self, event):
        def pressed(key):
            keys = pygame.key.get_pressed()
            return keys[key]

        if pressed(K_UP):
            self.selectedMenu = (self.selectedMenu - 1) % len(self.menus)
            self._updateSelectedMenu()

        if pressed(K_DOWN):
            self.selectedMenu = (self.selectedMenu + 1) % len(self.menus)
            self._updateSelectedMenu()

        if pressed(K_SPACE) or pressed(K_RETURN) or pressed(K_x):
            if len(self.menus):
                self.menus[self.selectedMenu].click()

        if event.type == pygame.QUIT or pressed(K_ESCAPE):
            pygame.quit()
            sys.exit()


    def addMenu(self, caption, antialias=False, color=(255, 255, 255), activeColor=(255, 0, 255)):
        self.menus.append(MenuItemClass(caption, antialias=antialias, color=color, activeColor=activeColor))

        # update placement (center)
        objAmount = len(self.menus) + 1
        for i in range(len(self.menus)):
            self.menus[i].rect.centerx = WINWIDTH / 2
            self.menus[i].rect.centery = WINHEIGHT / (objAmount + 1) * (i + 2)

        self._updateSelectedMenu()

    def _updateSelectedMenu(self):
        for menu in self.menus:
            if self.menus.index(menu) == self.selectedMenu:
                menu.select()
            else:
                menu.deselect()


class MenuItemClass(pygame.sprite.Sprite):
    def __init__(self, caption, antialias=False, color=(255, 255, 255), activeColor=(255, 0, 255)):
        pygame.sprite.Sprite.__init__(self)

        self.caption = caption
        self.antialias = antialias
        self.color = color
        self.activeColor = activeColor

        self.font = pygame.font.Font(filepath('Minecraftia.ttf'), 32)

        self.image = self.font.render(self.caption, self.antialias, self.color)
        self.rect = self.image.get_rect()

        self.event = None

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def select(self):
        self.image = self.font.render(
            self.caption, self.antialias, self.activeColor)

    def deselect(self):
        self.image = self.font.render(
            self.caption, self.antialias, self.color)

    def click(self):
        if self.event is not None:
            self.event()

    def connect(self, action):
        self.event = action


class MenuMain(MenuClass):
    def __init__(self, surface, engine):
        '''menus
        '''
        MenuClass.__init__(self, surface)

        self.engine = engine
        self.title = 'Adventure 2D'

        self.addMenu('Start')
        self.menus[0].connect(self.clickStart)

        self.addMenu('About')
        self.menus[1].connect(self.clickAbout)

        self.addMenu('Quit')
        self.menus[2].connect(self.clickQuit)

    def clickStart(self):
        self.engine.setState(MENU_SELECT)

    def clickAbout(self):
        self.engine.setState(MENU_ABOUT)

    def clickQuit(self):
        pygame.quit()
        sys.exit()


class MenuSelect(MenuClass):
    def __init__(self, surface, engine):
        '''menus
        '''
        MenuClass.__init__(self, surface)
        self.title = 'Select a Level'

        self.engine = engine

        self.addMenu('Level 1')
        self.menus[0].connect(self.click1)

        self.addMenu('Level 2')
        self.menus[1].connect(self.click2)

        self.addMenu('Level 3')
        self.menus[2].connect(self.click3)

        self.addMenu('back')
        self.menus[3].connect(self.back)

    def click1(self):
        self.engine.currentLevel = 1
        self.engine.setState(MENU_INGAME)

    def click2(self):
        self.engine.currentLevel = 2
        self.engine.setState(MENU_INGAME)

    def click3(self):
        self.engine.currentLevel = 3
        self.engine.setState(MENU_INGAME)

    def back(self):
        self.engine.setState(MENU_MAIN)

class MenuAbout(MenuClass):
    def __init__(self, surface, engine):
        '''menus
        '''
        MenuClass.__init__(self, surface)
        self.title = '@Kewei-cpu'

        self.engine = engine

        self.addMenu('back')
        self.menus[0].connect(self.back)

    def back(self):
        self.engine.setState(MENU_MAIN)


class MenuNext(MenuClass):
    def __init__(self, surface, engine):
        '''menus
        '''
        MenuClass.__init__(self, surface)

        self.engine = engine
        self.title = 'Level Completed in {} s'.format(round(level.levelTime, 1))

        self.addMenu('Next')
        self.menus[0].connect(self.next)

        self.addMenu('Back')
        self.menus[1].connect(self.back)


    def next(self):
        self.engine.currentLevel += 1
        self.engine.setState(MENU_INGAME)

    def back(self):
        self.engine.setState(MENU_SELECT)



class MenuLoss(MenuClass):
    def __init__(self, surface, engine):
        '''menus
        '''
        MenuClass.__init__(self, surface)

        self.engine = engine
        self.title = 'You Died !'

        self.addMenu('Retry')
        self.menus[0].connect(self.retry)

        self.addMenu('Back')
        self.menus[1].connect(self.back)

    def retry(self):
        self.engine.setState(MENU_INGAME)

    def back(self):
        self.engine.setState(MENU_SELECT)
