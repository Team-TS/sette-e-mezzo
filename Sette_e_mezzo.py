import random, pygame, sys 
from pygame.locals import *
from game import *
from display import *
from globalvars import *

# constants (CamelCase)
Name             =  "Sette e mezzo"
Game             =  GameInstance(Name,WindowWidth,WindowHeight)

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
                print("Game")
                selection = Game.runGame(7)
                if selection:
                        if selection == 1:
                                setMenuState()
                        if selection == 2:
                                setPostgameState()

        while inPostgameState():
                print("Postgame")
                Game.showPostgame()
                setMenuState()
