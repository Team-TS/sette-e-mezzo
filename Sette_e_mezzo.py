import random, pygame, sys 
from pygame.locals import *
from game import *
from display import *
from globalvars import *

# constants (CamelCase)
Name             =  "Sette e mezzo"
Game             =  GameInstance(Name,globalvars.WindowWidth,globalvars.WindowHeight)

# game states and player
run = True

while run:
        if getAppState() == STATE_KILL:
                run = False

        while inMainMenuState():
                print("Menu")
                menu = Game.showMenu()
                if menu:
                        if menu == 1:
                                run = False                                
                        if menu == 2:
                                setGameState()

        while inGameState():
                print("game")
                Game.runGame()
                setMenuState()