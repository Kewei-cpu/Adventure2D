from game.constants import WINWIDTH, WINHEIGHT
from game.engine import GameEngine


def main():
    gameEngine = GameEngine(WINWIDTH, WINHEIGHT)
    gameEngine.initializeGame()
