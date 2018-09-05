import pygame
from pygame.locals import *
from probability import prob
class Initiate:

	def __init__(self,name,w,h):
		pygame.init()
		pygame.display.set_caption(name)
		pygame.display.set_icon(pygame.image.load("images/icon.png"))
		self.display = pygame.display.set_mode((w,h))
		self.fps     =  pygame.time.Clock()


	def events(self):
		return pygame.event.get()

	def quit(self):
		pygame.quit()

	def update(self,speed):
		self.fps.tick(speed)
		pygame.display.update()

	def vistext(self,TextObj,txt,color):
		surface          = TextObj.font.render(str(txt),True,color,TextObj.background)
		position         = surface.get_rect()
		position.topleft = TextObj.pos
		self.display.blit(surface,position)

	def vissurf(self,surface,pos):
		position         = surface.get_rect()
		position.topleft = pos
		self.display.blit(surface,position)


class Card:

	def __init__(self,code,suit,value,name):
		self.code  = code
		self.suit  = suit
		self.value = value
		self.name  = name
		self.img   = pygame.image.load("images/" + code + ".png")

#class Button:

class Deck:
<<<<<<< HEAD
	
	img = pygame.image.load("images/deck.jpg")

	def __init__(self, name = "Deck", forge = True):

		self.name = ""
		self.cards = []

=======
	img = pygame.image.load("images/deck.jpg")

	def __init__(self, name = "Deck", forge = True):
		self.name = ""
		self.cards = []
>>>>>>> 02ffa61690f53e0b691b57b33280ab17ff9d10b0
		if forge:
			print("Forging cards {0}".format(self.name))
			self.forge_cards()
		if name:
			self.name = name
		
		print("Initialized new Deck ({0})with cards: ({1})".format(self.name, len(self.cards)))

	def forge_cards(self):
		file_read = [i.split(",") for i in open("values.txt").read().split("\n")]
		for line in file_read:
			card = Card(line[0], line[1], line[2], line[3])
			self.cards.append(card)

	def draw_card(self):
		if len(self.cards):
			card = self.cards.pop()
			return card


	def shuffle(self):
		shuffled_deck = []
		while len(self.cards):
			for card in self.cards:
				if prob(30):
					self.cards.remove(card)
					shuffled_deck.append(card)
		self.cards = shuffled_deck

class Text:
	
	def __init__(self,pos,font,size,background = False):
		self.background = background
		self.pos  = pos
		self.font = pygame.font.Font("fonts/" + font + ".ttf",size)
	

	







