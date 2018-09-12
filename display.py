import pygame
from pygame.locals import *
import globalvars
from game import *
import math


class GameInstance:
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
		globalvars.state = globalvars.STATE_KILL
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

	def showMenu(self):
		while True:
			self.display.fill((255, 255, 255))
			PlayButton = Button((497,349),globalvars.StdFont,30,globalvars.GREEN,"Play",globalvars.YELLOW,globalvars.CYAN)
			QuitButton = Button((497,429), globalvars.StdFont,30, globalvars.BLACK, "Quit", globalvars.BLUE, globalvars.CYAN)
			self.visbutton(QuitButton)
			self.visbutton(PlayButton)
			self.update(globalvars.GameSpeed)

			for event in self.events():
				if event.type == pygame.QUIT or QuitButton.check(event):
					self.quit()
					return 1
				if PlayButton.check(event):
					return 2
					
	def runGame(self, numbots):
		running = True
		my_player = Player("My Name")
		gamestate = GameState([my_player], numbots)
		gamestate.startGame()
		playarea = PlayArea(gamestate.players, self)
		gamestate.waitforplayer = True

		while running and gamestate:
			# Draw the screen and controls
			self.display.fill(globalvars.WHITE)
			DrawButton = Button((330,700),globalvars.StdFont,30,globalvars.GREEN,"Draw",globalvars.YELLOW,globalvars.CYAN)
			self.visbutton(DrawButton)
			StayButton = Button((630,700),globalvars.StdFont,30,globalvars.GREEN,"Stay",globalvars.YELLOW,globalvars.CYAN)
			self.visbutton(StayButton)

			#Draw the card areas and cards

			for loc in playarea.locs:
				coords = playarea.locs[loc]
				self.display.blit(globalvars.playerimg, coords)

			if not gamestate.waitforplayer:
				gamestate.fire()

			self.update(globalvars.GameSpeed)


			# Event handling
			for event in self.events():
				if event.type == pygame.QUIT:
					self.quit()
					return 0
				if DrawButton.check(event):
					print("Draw event fired")
				if StayButton.check(event):
					print("Stay event fired")





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

	def render(self):
		"""Render the button to the screen"""

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

class PlayArea():
	def __init__(self, players,surface):
		# Calculate the correct distribution of players
		circle = 360
		angle = circle / len(players)
		print(len(players))
		radian = angle * 0.0174532925
		radangle = radian
		radius = 250
		self.locs = {}

		for player in players:
			x = (radius * math.cos(radangle)) + (globalvars.WindowWidth / 2) - 58
			y = (radius * math.sin(radangle)) + (globalvars.WindowHeight / 2) - 57

			print("Location for {0} - {1},{2}".format(player.name, math.floor(x), math.floor(y)))
			coords = (x, y)
			self.locs[player] = coords
			radangle += radian
		
		print(self.locs)


class PlayerArea():
	def __init__(self):
		return