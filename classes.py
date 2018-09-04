import pygame
from pygame.locals import *
class Card:

	def __init__(self,code,suit,value,name):
		self.code  = code
		self.suit  = suit
		self.value = value
		self.name  = name
		self.img   = pygame.image.load("images/" + code + ".png")
		self.drawn = False

#class Button:

class Deck:
	name = "Deck"
	cards = []
	img = pygame.image.load("images/deck.jpg")

	def __init__(self):
		self.forge_cards()

	def forge_cards(self):
		file_read = [i.split(",") for i in open("values.txt").read().split("\n")]
		for line in file_read:
			card = Card(line[0], line[1], line[2], line[3])
			self.cards.append(card)
			
			