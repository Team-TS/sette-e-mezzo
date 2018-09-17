from pygame import image
from os import path

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

StdFont          =  "Archivo-SemiBold"
GameSpeed        =  60
WindowWidth      =  1024
WindowHeight     =  768

#Load files once.

playerimg = image.load(path.join('images', 'avatar.png'))
facedownimg = image.load(path.join('images', 'cards', 'cardback.png'))
cardvalues = [i.split(",") for i in open("values.txt").read().split("\n")]
cardimages = {}
botnames = ["Terry", "Hannah", "Steve", "Mark", "James", "Jed", "Rachael", "Brian", "Chadwick", "Wolfgang"]

def loadCardImages():
    for card in cardvalues:
        img_code = card[0]
        img = image.load(path.join('images', 'cards', img_code + '.png'))
        cardimages[img_code] = img

loadCardImages()

STATE_KILL = 0
STATE_MENU = 1
STATE_GAME = 2
STATE_POST = 3

state = STATE_MENU

def inMainMenuState():
    if state == STATE_MENU:
        return True

def inGameState():
    if state == STATE_GAME:
        return True

def inPostgameState():
    if state == STATE_POST:
        return True

def getAppState():
    return state

def setMenuState():
    global state
    state = STATE_MENU

def setGameState():
    global state
    state = STATE_GAME

def setPostgameState():
    global state
    state = STATE_POST