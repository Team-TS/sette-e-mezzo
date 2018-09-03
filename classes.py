import pygame
from pygame.locals import *
class Card:

	def __init__(self,code,suit,value,name):
		self.code  = code
		self.suit  = suit
		self.value = value
		self.name  = name
		self.img   = pygame.image.load(code + ".png")
		self.drawn = False

#class Button:

