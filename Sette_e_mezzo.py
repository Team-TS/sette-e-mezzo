import random, pygame, sys 
from pygame.locals import *
from game import *
from display import *


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
WindowWidth      =  1024
WindowHeight     =  768
GameSpeed        =  60
Game             =  Initiate(Name,WindowWidth,WindowHeight)
StdFont          =  "Archivo-SemiBold"  
CardText         =  Text((5,5),StdFont,20,BLACK)
DeckText         =  Text((550,300),StdFont,20,BLACK)
ScoreText        =  Text((50,300),StdFont,20,GREEN)
EndText          =  Text((200,300),StdFont,20,GREEN)
DealButton       =  Button((350,250),StdFont,30,RED,"Deal",CYAN,PURPLE)
PlayButton       =  Button((350,200),StdFont,30,GREEN,"Play",YELLOW,CYAN)
ResetButton      =  Button((350,250),StdFont,30,RED,"Reset",BLUE,CYAN)


# throwaways (lowercase)
gamestate = None
my_player = None

# outside game loop
while True:

        if not gamestate:

                player = Player("Me")
                my_player = player
                gamestate = GameState([player])
        
        # User input
        for event in Game.events():
                if event.type == QUIT:
                        Game.quit()
                        sys.exit()
                if PlayButton.check(event) == True:
                        gamestate.startGame()

        # Background 
        Game.display.fill(WHITE)

        # print items to the screen
        Game.visbutton(PlayButton)

        # Refresh screen
        Game.update(GameSpeed)

        if ResetButton.state:
                ResetButton.state = False
        if not DealButton.state:
                DealButton.state = True


        # Main game loop
        while gamestate.isrunning:

                # User input
                for event in Game.events():
                        if event.type == QUIT:
                                Game.quit()
                                sys.exit()
                        if DealButton.check(event) == True and gamestate and gamestate.isrunning:
                                gamestate.dealCards()
                        if ResetButton.check(event) == True and gamestate and gamestate.isrunning:
                                gamestate.endGame()

                # Render background               
                Game.display.fill(WHITE)

                        
                # --print the cards and info to the display surface--

                # latest card name and value
                if my_player and len(my_player.deck.cards):
                        Game.vistext(CardText,my_player.deck.cards[-1].name + " " + my_player.deck.cards[-1].value)



                # score
                if my_player:
                        if my_player.score <= 7.5:
                                scorecolor = GREEN
                        else:
                                scorecolor = RED

                        Game.vistext(ScoreText,"Score: " + str(my_player.score if my_player else 0), scorecolor)
                        if my_player.score > 7.5:
                                Game.vistext(EndText,"You lost! Score over 7.5!",scorecolor)
                                tmp_count = 0
                                for card in my_player.deck.cards:
                                        Game.vissurf(card.img,((60*tmp_count),50))
                                        Game.vistext(Text(((18 + 60*tmp_count),160),StdFont,20,scorecolor,GRAY),card.code)
                                        tmp_count = tmp_count + 1
                                

                tmp_count = 0
                # cards and codes
                if gamestate and gamestate.isrunning:
                        if my_player:
                                for card in my_player.deck.cards:
                                        Game.vissurf(card.img,((60*tmp_count),50))
                                        Game.vistext(Text(((18 + 60*tmp_count),160),StdFont,20,scorecolor,GRAY),card.code)
                                        tmp_count = tmp_count + 1


                        # remaining deck
                        if my_player:
                                Game.vissurf(gamestate.dealer.deck.img, DeckText.xy)
                                Game.vistext(DeckText,"Remaining deck = " + str(len(gamestate.dealer.deck.cards)))

                                
                                # keep score
                                gamestate.updateScore()
                                if my_player and my_player.score > 7.5:
                                        print("Score over 7.5, you are bust!")
                                        DealButton.state = False
                                        ResetButton.state = True
                                        


                # Buttons
                Game.visbutton(DealButton)
                Game.visbutton(ResetButton)


                # process game tik
                Game.update(GameSpeed)

