import pygame
from pygame.locals import *
from probability import prob


class Initiate:

	def __init__(self,name,w,h):
		pygame.init()
		pygame.display.set_caption(name)
		pygame.display.set_icon(pygame.image.load("images/icon.png"))
		self.display = pygame.display.set_mode((w,h))
		self.fps     = pygame.time.Clock()

	def events(self):
		return pygame.event.get()

	def quit(self):
		pygame.quit()

	def vistext(self,TextObj,txt,colour = False):
		if not colour:
			surface = TextObj.font.render(str(txt),True,TextObj.colour,TextObj.background)
		else:
			surface = TextObj.font.render(str(txt),True,colour,TextObj.background)

		position         = surface.get_rect()
		position.topleft = TextObj.xy
		self.display.blit(surface,position)

	def vissurf(self,surface,xy):
		position         = surface.get_rect()
		position.topleft = xy
		self.display.blit(surface,position)

	def update(self,speed):
		self.fps.tick(speed)
		pygame.display.update()


class Card:

	def __init__(self,code,suit,value,name):
		self.code  = code
		self.suit  = suit
		self.value = value
		self.name  = name
		self.img   = pygame.image.load("images/" + code + ".png")


class Deck:
	
	img = pygame.image.load("images/deck.jpg")

	def __init__(self, name = "Deck", forge = True):

		self.name = ""
		self.cards = []

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
	
	def __init__(self,xy,font,size,colour,background = False):
		self.background = background
		self.xy         = xy
		self.font       = pygame.font.Font("fonts/" + font + ".ttf",size)
		self.colour     = colour
	

class Button(Text):

	def __init__(self,xy,font,size,colour,txt,background,hover):
		Text.__init__(self,xy,font,size,colour,background)
		self.hover            = hover
		self.txt              = txt
		self.state            = 0
		self.surface          = self.font.render(str(self.txt),True,self.colour,self.background)
		self.position         = self.surface.get_rect()
		self.position.topleft = self.xy

	def check(self,event):

		if event.type == MOUSEBUTTONUP:
			if self.position.collidepoint(event.pos):
				return True
	          
		if event.type == MOUSEMOTION or event.type == MOUSEBUTTONDOWN:
			if self.position.collidepoint(event.pos):
				self.surface = self.surface = self.font.render(str(self.txt),True,self.colour,self.hover)
			else:
				self.surface = self.font.render(str(self.txt),True,self.colour,self.background)

      










