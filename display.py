import pygame
from pygame.locals import *

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
