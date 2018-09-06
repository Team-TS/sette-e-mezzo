import random, pygame, sys 
from pygame.locals import *
from classes import *


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
GameSpeed        =  20
Game             =  Initiate(Name,WindowWidth,WindowHeight)
StdFont          =  "Archivo-SemiBold"  
CardNames        =  Text((5,5),StdFont,20,BLACK)
DeckInfo         =  Text((300,300),StdFont,20,BLACK)
ScoreInfo        =  Text((100,300),StdFont,20,GREEN)




# throwaways (lowercase)
deal = True
hand = Deck("Your hand", forge = False)
available = []

# Game loop
while True:

        # available cards 
        if not available:
                available = Deck("Dealer")
    
        # User input
        for event in Game.events():
                if event.type == QUIT:
                        Game.quit()
                        sys.exit()
                if event.type == KEYDOWN:
                        if event.key == K_SPACE:
                                deal = True

                        
        # white background               
        Game.display.fill(WHITE)
        
        # deal a new card
        if deal == True and len(available.cards):
                newcard = available.draw_card()
                hand.cards.append(newcard)
                deal = False
        
        # keep score
        score = sum([float(card.value) for card in hand.cards])

        # --print the cards info to the display surface--

        # latest card name and value
        if len(hand.cards):
                Game.vistext(CardNames,hand.cards[-1].name + " " + hand.cards[-1].value)


        # score
        if score <= 7.5:
                scorecolor = GREEN
        else:
                scorecolor = RED

        Game.vistext(ScoreInfo,"Score: " + str(score), scorecolor)

        tmp_count = 0
        # cards and codes
        for card in hand.cards:
                Game.vissurf(card.img,((60*tmp_count),50))
                Game.vistext(Text(((18 + 60*tmp_count),160),StdFont,20,scorecolor,GRAY),card.code)
                tmp_count = tmp_count + 1

        
        # remaining deck
        Game.vissurf(available.img, DeckInfo.pos)
        Game.vistext(DeckInfo,"Remaining deck = " + str(len(available.cards)))

        # process game tik
        Game.update(GameSpeed)

