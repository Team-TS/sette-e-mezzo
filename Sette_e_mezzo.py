import random, pygame, sys 
from pygame.locals import *
from classes import *
from time import sleep


# Colour variables (UPPERCASE)
#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)
BLACK    = (  0,   0,   0)

# constants (CamelCase)
Name             =  "Sette e mezzo"
WindowWidth      =  800
WindowHeight     =  500
GameSpeed        =  60
Game             =  Initiate(Name,WindowWidth,WindowHeight)
StdFont          =  "Archivo-SemiBold"  
CardText         =  Text((5,5),StdFont,20,BLACK)
DeckText         =  Text((300,300),StdFont,20,BLACK)
ScoreText        =  Text((100,300),StdFont,20,GREEN)
DealButton       =  Button((400,250),StdFont,30,RED,"Deal",CYAN,PURPLE)


# throwaways (lowercase)
deal = True
gamestate = None
my_player = None

# Game loop
while True:

        if not gamestate:
                #Need a menu here really.
                player = Player("Me")
                my_player = player
                gamestate = GameState(player)
    
        # User input
        for event in Game.events():
                if event.type == QUIT:
                        Game.quit()
                        sys.exit()
                if DealButton.check(event) == True and gamestate and gamestate.isrunning:
                        gamestate.dealCards()




                      
        # white background               
        Game.display.fill(WHITE)

                
        # --print the cards info to the display surface--

        # latest card name and value
        if my_player and len(my_player.deck.cards):
                Game.vistext(CardNames,my_player.deck.cards[-1].name + " " + my_player.deck.cards[-1].value,BLACK)


        # score
        if my_player:
                if my_player.score <= 7.5:
                        scorecolor = GREEN
                else:
                        scorecolor = RED

                Game.vistext(ScoreInfo,"Score: " + str(my_player.score if my_player else 0), scorecolor)
                if my_player.score > 7.5:
                        Game.vistext(Text((250,300),StdFont,20),"You lost! Score over 7.5!", scorecolor)
                        tmp_count = 0
                        for card in my_player.deck.cards:
                                Game.vissurf(card.img,((60*tmp_count),50))
                                Game.vistext(Text(((18 + 60*tmp_count),160),StdFont,20,GRAY),card.code,scorecolor)
                                tmp_count = tmp_count + 1
                        

        tmp_count = 0
        # cards and codes
        if gamestate and gamestate.isrunning:
                if my_player:
                        for card in my_player.deck.cards:
                                Game.vissurf(card.img,((60*tmp_count),50))
                                Game.vistext(Text(((18 + 60*tmp_count),160),StdFont,20,GRAY),card.code,scorecolor)
                                tmp_count = tmp_count + 1


                # remaining deck
                if my_player:
                        Game.vissurf(gamestate.dealer.deck.img, DeckInfo.pos)
                        Game.vistext(DeckInfo,"Remaining deck = " + str(len(gamestate.dealer.deck.cards)), BLACK)

                        
                        # keep score
                        gamestate.updateScore()
                        if my_player and my_player.score > 7.5:
                                print("Score over 7.5, ending game!")
                                gamestate.endGame()


        # process game tik
        Game.update(GameSpeed)

