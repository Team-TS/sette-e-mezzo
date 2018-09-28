import pygame
import probability
from random import choice
import globalvars

class GameState:
	"""Class for the state of a game, keeps track of players involved, dealer etc. Pass a list of players as argument."""
	name = "GameState"

	def __init__(self):
		self.players = []
		self.my_player = None
		self.isrunning = False
		self.dealer = None
		self.waitforplayer = False
		self.tick = 0
		self.botnames = globalvars.botnames.copy()
		self.gamelog = []
		self.logGame("Setting up game.")

	def setupPlayers(self,player_name,bots = 0):
		# setup opponents 
		if bots:
			while bots > 0:
				TheBot = BotPlayer(self.botnames, self)
				self.players.append(TheBot)
				bots -= 1

		if len(self.players) < 2:
			""" We can't play alone"""
			enemy = BotPlayer(choice(["Mark", "Emily", "Steve", "Amy"]), self)
			self.dealer = enemy
			self.players.append(enemy)
		else:
			dealer = choice(self.players)
			dealer.makeDealer()
			self.dealer = dealer

		# setup your player (currently player cannot be dealer)
		self.my_player = Player(player_name)
		self.my_player.isme = True
		self.players.append(self.my_player)

		self.logGame("Setting up players.")

	def fire(self):
		"""One iteration of the game ticker"""
		self.tick = self.tick + 1

		if self.tick == 1:
			print("Setting up game, dealing cards to all players.")
			self.dealCards()
			self.waitforplayer = True
			return

		if self.waitforplayer:
			return

		for player in self.players:
			if player.isdealer:
				continue
			if player.playing:
				player.action(self)

		self.waitforplayer = True


	def addPlayers(self, player):
		"""Takes a list of players, adds them to the existing game."""
		self.players.append(player)

	def removePlayer(self, player):
		"""Sets the player as not playing (out)"""
		player.playing = False
	
	def setDealer(self, player):
		"""Argument must be a Player object, replaces dealer with this player"""
		print("setting dealer " + player.name)
		if self.dealer:
			self.players.append(self.dealer)
			self.dealer = None
		if player:
			self.dealer = player
		if player in self.players:
			self.players.remove(player)
	
	def dealCards(self):
		"""The dealer will deal cards to all players present at the table except himself"""
		if not self.dealer:
			print("No dealer present")
			return False

		for player in self.players:
			if player.isdealer:
				continue
			dealtcard = self.dealer.deck.draw_card()
			if player.isme:
				dealtcard.setFaceUp()
			self.logGame("Dealer {0} dealt {1} to {2}".format(self.dealer.name, dealtcard.name, player.name))
			print("Dealer {0} dealt {1} to {2}".format(self.dealer.name, dealtcard.name, player.name))
			player.receiveCard(dealtcard)
			


	def dealToPlayer(self, player):
		"""The dealer deals a card to the player face up"""
		if not player.isbust or not player.isstay:
			card = self.dealer.deck.draw_card()
			card.setFaceUp()
			self.logGame("Dealer {0} dealt {1} to {2}".format(self.dealer.name, card.name, player.name))
			print("Dealer {0} dealt {1} to {2}".format(self.dealer.name, card.name, player.name))
			player.receiveCard(card)
	
	def updateScore(self):
		"""Updates the scores of all players"""
		for player in self.players:
			player.updateScore() 

	def startGame(self):
		"""Starts the game"""
		self.logGame("Game starting...")
		self.isrunning = True

 
	def resetGame(self, resetdealer = True):
		"""Ends the game and resets dealer/players"""
		for player in self.players:
			if not player.isdealer:
				player.resetPlayer()
			elif resetdealer:
				player.resetPlayer()

		self.isrunning = False

	def getDealtFaceUps(self):
		faceups = []
		for player in self.players:
			faceups = player.deck.getFaceUps()
		return faceups

	def getFaceDowns(self):
		facedowns = []
		for player in self.players:
			for card in player.getFaceDowns():
				facedowns.append(card)
		return facedowns

	def logGame(self, logentry):
		self.gamelog.append(str(logentry))


class Player:
	"""Class for an individual player, expandable for adding AI later, attibs are: name (str), deck (Deck obj), score (num)"""

	def __init__(self, name, gamestate = None, dealer = False):
		self.name = name
		self.score = 0
		self.playing = True
		self.isbust = False
		self.isstay = False
		self.isme = False
		self.cardarea = None
		self.loc = None
		self.gameplaying = None # Store the gamestate here in which the player is in.
		if not dealer:
			self.deck = Deck("My Deck", False)
			self.isdealer = False
		else:
			self.deck = Deck("Dealer's deck")
			self.isdealer = True
			self.playing  = False

	def makeDealer(self):
		self.deck = Deck("Dealer's deck")
		self.isdealer = True
		self.playing = False

	def setGamestate(self, gamestate):
		self.gameplaying = gamestate
	
	def action(self, gamestate):
		return
	
	def getCards(self):
		return self.deck.cards

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
			self.score = sum([float(card.value) for card in self.getCards()])
		else:
			print("Dealer cannot have a score")
			return False

	def resetPlayer(self):
		"""resets a players score and deck"""
		self.score = 0
		self.isbust = False
		self.isstay = False
		if not self.isdealer:
			self.deck = Deck("My Deck", False)
			self.playing = True
		else:
			self.deck = Deck("Dealer's deck")
			self.playing = False

	def stay(self, gamestate):
		print(self.name + " stayed.")
		self.isstay = True
		self.playing = False
		gamestate.logGame("{0} stayed.".format(self.name))
		return

	def bust(self, gamestate):
		print(self.name + " went bust!")
		for card in self.deck.cards:
			if not card.faceup:
				card.setFaceUp()
		self.playing = False
		self.isbust = True
		gamestate.logGame("{0} went bust!".format(self.name))
		#gamestate.removePlayer(self)
		return


	def checkWinCondition(self):
		score = sum([float(card.value) for card in self.getCards()])
		if score == 7.5:
			return True

	def checkLoseCondition(self):
		score = sum([float(card.value) for card in self.getCards()])
		if score > 7.5:
			return True

	def getFaceDowns(self):
		return [card for card in self.deck.cards if card.faceup == False]

class BotPlayer(Player):
	botrisks = [3, 5, 7, 10, 15, 20, 30, 40, 50, 60]
	def __init__(self,botnames, gamestate = None, name = None):
		super().__init__("Bot", gamestate)
		if name:
			self.name = name
		else:
			self.name = choice(botnames)
			botnames.remove(self.name)
			print("No name provided for bot: selecting {0}".format(self.name))
		self.risk = choice(self.botrisks)
		self.avatar = pygame.image.load("images/avatar.png")

	def action(self, gamestate):
		self.reviewHand(gamestate)
	
	def reviewHand(self, gamestate):
		my_hand = sum([float(card.value) for card in self.getCards()])
		target_score = float(7.5)
		score_to_get = target_score - my_hand

		if self.checkWinCondition():
			self.playing = False
			#return self.win(gamestate)

		faceups = list(gamestate.getDealtFaceUps())
		potential_cards = Deck(silent = True).cards

		# Remove cards which we *know* have been played from the list of potentials still in play

		for card in faceups:
			for pot_card in potential_cards:
				if card.code == pot_card.code: # ugh, a better way to do this maybe?
					potential_cards.remove(pot_card)
		
		# Work out the probabilty of drawing exactly what we need to win, or drawing lower...

		if probability.probDrawExactValue(score_to_get, potential_cards) * 100 > self.risk or probability.probDrawValueOrLess(score_to_get, potential_cards) * 100 > self.risk:
			self.draw(gamestate)
			if self.checkLoseCondition():
				self.bust(gamestate)
			return

		# So we didn't want to draw in either case. Let's pass instead.
		return self.stay(gamestate)
		
	def win(self, gamestate):
		print(self.name + " Won the game!")
		gamestate.endGame(reset = False)
		return
	
	def draw(self, gamestate):
		print(self.name + " drew a card")
		gamestate.dealToPlayer(self)
		return

class Card:
	"""Basic class for storing card attributes"""

	def __init__(self,code,suit,value,name):
		self.code  = code
		self.suit  = suit
		self.value = value
		self.name  = name
		self.img   = globalvars.cardimages[code]
		self.faceup = False
	
	def setFaceUp(self):
		self.faceup = True
	
	def flip(self):
		self.faceup = not self.faceup

	def setFaceDown(self):
		self.faceup = False


class Deck:
	"""Class for loading managing and manipulating a list of Card objects"""

	def __init__(self, name = "Deck", forge = True, shuffle = True, silent = False):

		self.name = ""
		self.cards = []

		if forge:
			self.forge_cards()
		if shuffle:
			self.shuffle()
		if name:
			self.name = name

		if not silent:
			print("Initialized new Deck ({0})with cards: ({1})".format(self.name, len(self.cards)))

	def forge_cards(self):
		"""Spawns a new list of cards and adds them to the deck, card values taken from values.txt"""
		for line in globalvars.cardvalues:
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
				if probability.prob(30):
					self.cards.remove(card)
					shuffled_deck.append(card)
		self.cards = shuffled_deck

	def getFaceUps(self):
		cards = []
		for card in self.cards:
			if card.faceup:
				cards.append(card)
		return cards
