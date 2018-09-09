import pygame
from pygame.locals import *
from probability import prob
from random import choice

class Initiate:
	""" Class for handelling pygame init() and other pygame modules"""

	def __init__(self,name,w,h):
		pygame.init()
		pygame.display.set_caption(name)
		pygame.display.set_icon(pygame.image.load("images/icon.png"))
		self.display = pygame.display.set_mode((w,h))
		self.fps     = pygame.time.Clock()

	def events(self):
		"""returns a list of pygame events"""
		return pygame.event.get()

	def quit(self):
		"""Closes the application"""
		pygame.quit()

	def vistext(self,TextObj,txt,colour = False):
		"""Renders given text to screen using preferences stored in a Text object"""
		if not colour:
			surface = TextObj.font.render(str(txt),True,TextObj.colour,TextObj.background)
		else:
			surface = TextObj.font.render(str(txt),True,colour,TextObj.background)

		position         = surface.get_rect()
		position.topleft = TextObj.xy
		self.display.blit(surface,position)

	def vissurf(self,surface,xy):
		"""Renders the given pygame surface to the screen at given xy co-ordinate"""
		position         = surface.get_rect()
		position.topleft = xy
		self.display.blit(surface,position)

	def visbutton(self,button):
		"""Renders an interactive Button object"""
		if button.state == True:
			self.display.blit(button.surface,button.position)

	def update(self,speed):
		"""Updates screen"""
		self.fps.tick(speed)
		pygame.display.update()


class GameState:
	"""Class for the state of a game, keeps track of players involved, dealer etc. Pass a list of players as argument."""
	name = "GameState"

	def __init__(self, players):
		self.players = [players]
		self.isrunning = False
		self.dealer = None
		if len(self.players) < 2:
			""" We can't play alone"""
			enemy = Player(choice(["Mark", "Emily", "Steve", "Amy"]), True)
			self.dealer = enemy
		else:
			dealer = choice(players)
			self.dealer = dealer

	def addPlayers(self, player):
		"""Takes a list of players, adds them to the existing game."""
		self.players.append(player)
	
	def setDealer(self, player):
		"""Argument must be a Player object, replaces dealer with this player"""
		if self.dealer:
			self.players.append(self.dealer)
			self.dealer = None
		if player:
			self.dealer = player
		if player in self.players:
			self.players.remove(player)
	
	def dealCards(self):
		"""The dealer will deal cards to all players present at the table"""
		if not self.dealer:
			print("No dealer present")
			return False

		if not len(self.dealer.deck.cards): # temporary solution 
			self.endGame(True)
			print("Out of cards, reseting deck")
		
		for player in self.players:
			dealtcard = self.dealer.deck.draw_card()
			print("Dealer {0} dealt {1}".format(self.dealer.name, dealtcard.name))
			player.receiveCard(dealtcard)
	
	def updateScore(self):
		"""Updates the scores of all players"""
		for player in self.players:
			player.updateScore()

	def startGame(self):
		"""Starts the game"""
		self.isrunning = True

	def endGame(self, resetdealer = False):
		"""Ends the game and resets non dealer players"""
		for player in self.players:
			player.resetPlayer()

		if resetdealer:
			self.dealer.resetPlayer()

		self.isrunning = False






class Player:
	"""Class for an individual player, expandable for adding AI later, attibs are: name (str), deck (Deck obj), score (num)"""

	def __init__(self, name, dealer = False):
		self.name = name
		self.score = 0
		if not dealer:
			self.deck = Deck("My Deck", False)
			self.isdealer = False
		else:
			self.deck = Deck("Dealer's deck")
			self.isdealer = True

	def adjustScore(self, adj):
		"""Adjusts score by X"""
		self.score = self.score + adj
	
	def receiveCard(self, card):
		"""adds the given card to the players deck"""
		self.deck.addCard(card)
		return True

	def updateScore(self):
		"""calculates the player score based on cards in their deck(hand)"""
		if not self.isdealer:
			self.score = sum([float(card.value) for card in self.deck.cards])
		else:
			print("Dealer cannot have a score")
			return False

	def resetPlayer(self):
		"""resets a players score and deck"""
		if not self.isdealer:
			self.deck = Deck("My Deck", False)
		else:
			self.deck = Deck("Dealer's deck")



class Card:
	"""Basic class for storing card attributes"""

	def __init__(self,code,suit,value,name):
		self.code  = code
		self.suit  = suit
		self.value = value
		self.name  = name
		self.img   = pygame.image.load("images/" + code + ".png")


class Deck:
	"""Class for loading managing and manipulating a list of Card objects"""
	img = pygame.image.load("images/deck.jpg")

	def __init__(self, name = "Deck", forge = True, shuffle = True):

		self.name = ""
		self.cards = []

		if forge:
			print("Forging cards {0}".format(self.name))
			self.forge_cards()
		if shuffle:
			self.shuffle()
		if name:
			self.name = name
		
		print("Initialized new Deck ({0})with cards: ({1})".format(self.name, len(self.cards)))

	def forge_cards(self):
		"""Spawns a new list of cards and adds them to the deck, card values taken from values.txt"""
		file_read = [i.split(",") for i in open("values.txt").read().split("\n")]
		for line in file_read:
			card = Card(line[0], line[1], line[2], line[3])
			self.addCard(card)

	def addCard(self, card):
		"""Adds passed card to the top of the deck"""
		self.cards.append(card)

	def draw_card(self):
		"""Returns a card from the top of the deck"""
		if len(self.cards):
			card = self.cards.pop()
			return card

	def shuffle(self):
		"""Shuffles the deck"""
		shuffled_deck = []
		while len(self.cards):
			for card in self.cards:
				if prob(30):
					self.cards.remove(card)
					shuffled_deck.append(card)
		self.cards = shuffled_deck


class Text:
	"""Basic class for storing text values such as location font and colour"""
	
	def __init__(self,xy,font,size,colour,background = False):
		self.background = background
		self.xy         = xy
		self.colour     = colour
		self.font       = pygame.font.Font("fonts/" + font + ".ttf",size)
		
	

class Button(Text):
	"""Extrapolation on the Text class which facilitates user input"""

	def __init__(self,xy,font,size,colour,txt,background,hover):
		Text.__init__(self,xy,font,size,colour,background)
		self.hover            = hover
		self.txt              = txt
		self.state            = True
		self.surface          = self.font.render(str(self.txt),True,self.colour,self.background)
		self.position         = self.surface.get_rect()
		self.position.topleft = self.xy

	def check(self,event):
		"""Returns True for a mouse click on the button"""

		if self.state:

			if event.type == MOUSEBUTTONUP:
				if self.position.collidepoint(event.pos):
					return True
		          
			if event.type == MOUSEMOTION or event.type == MOUSEBUTTONDOWN:
				if self.position.collidepoint(event.pos):
					self.surface = self.surface = self.font.render(str(self.txt),True,self.colour,self.hover)
				else:
					self.surface = self.font.render(str(self.txt),True,self.colour,self.background)

      










