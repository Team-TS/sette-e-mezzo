import pygame
from pygame.locals import *
from probability import prob
class Card:

	def __init__(self,code,suit,value,name):
		self.code  = code
		self.suit  = suit
		self.value = value
		self.name  = name
		self.img   = pygame.image.load("images/" + code + ".png")

#class Button:

class Deck:
	name = ""
	cards = []
	img = pygame.image.load("images/deck.jpg")

	def __init__(self, name = "Deck", forge = True):
		if forge:
			self.forge_cards()
		if name:
			self.name = name

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
