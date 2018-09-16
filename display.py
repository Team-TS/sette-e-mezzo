import pygame
from pygame.locals import *
import globalvars
from game import *
import math
import sys


class GameInstance:
	""" Class for handelling pygame init() and other pygame modules"""

	def __init__(self,name,w,h):
		pygame.init()
		pygame.display.set_caption(name)
		pygame.display.set_icon(pygame.image.load("images/icon.png"))
		self.display = pygame.display.set_mode((w,h))
		self.fps     = pygame.time.Clock()
		self.background = pygame.image.load("images/testbg.png")
		self.gamestate = None 

	def events(self):
		"""returns a list of pygame events"""
		return pygame.event.get()

	def quit(self):
		"""Closes the application"""
		globalvars.state = globalvars.STATE_KILL
		pygame.quit()
		sys.exit()


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

		PlayButton = Button((497,349),globalvars.StdFont,30,globalvars.GREEN,"Play",globalvars.YELLOW,globalvars.CYAN)
		QuitButton = Button((497,429), globalvars.StdFont,30, globalvars.BLACK, "Quit", globalvars.BLUE, globalvars.CYAN)

		while True:
			self.display.fill((255, 255, 255))
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
		my_player.isme = True
		self.gamestate = GameState([my_player], numbots)
		self.gamestate.startGame()
		playarea = PlayArea(self.gamestate.players, self)
		ExitButton = Button((30, 15), globalvars.StdFont, 30, globalvars.GREEN, "Quit", globalvars.YELLOW, globalvars.CYAN)
		StayButton = Button((630,700),globalvars.StdFont,30,globalvars.GREEN,"Stay",globalvars.YELLOW,globalvars.CYAN)
		DrawButton = Button((330,700),globalvars.StdFont,30,globalvars.GREEN,"Draw",globalvars.YELLOW,globalvars.CYAN)
		ResolveButton = Button((800,700),globalvars.StdFont,30,globalvars.GREEN,"Resolve",globalvars.YELLOW,globalvars.CYAN)
		ResolveButton.disable()

		while running and self.gamestate:
			if self.gamestate.isrunning:
				# Draw the screen and controls
				self.display.blit(self.background,(0,0))
				self.visbutton(DrawButton)
				self.visbutton(StayButton)
				self.visbutton(ResolveButton)
			
			self.visbutton(ExitButton)

			# check your players score
			if my_player.playing:
				if my_player.checkLoseCondition():
					my_player.bust(self.gamestate)

			# correct options
			if not my_player.playing:
				StayButton.disable()
				DrawButton.disable()
				ResolveButton.enable()

			#Draw the card areas and cards

			for loc in playarea.locs:
				coords = playarea.locs[loc]
				self.display.blit(globalvars.playerimg, coords)
			
			for area in playarea.cardareas:
				area.cardarea.render(self)

			if not self.gamestate.waitforplayer:
				self.gamestate.fire()

			# Player names
			y_offset = 110
			for player in self.gamestate.players:
				loc = (player.loc["x"], player.loc["y"] + y_offset)
				text = Text(loc, globalvars.StdFont,16,globalvars.BLACK)
				self.vistext(text, player.name)

			# Dealer
			loc = (self.gamestate.dealer.loc["x"], self.gamestate.dealer.loc["y"] + y_offset)
			text = Text(loc, globalvars.StdFont,16,globalvars.BLACK)
			self.vistext(text, self.gamestate.dealer.name + " the dealer")

			# player status
			y_offset = 50
			for player in self.gamestate.players:
				if player.isbust == True:
					loc = (player.loc["x"], player.loc["y"] - y_offset)
					text = Text(loc, globalvars.StdFont,16,globalvars.RED)
					self.vistext(text, "Bust")
				elif player.isstay == True:
					loc = (player.loc["x"], player.loc["y"] - y_offset)
					text = Text(loc, globalvars.StdFont,16,globalvars.ORANGE)
					self.vistext(text, "Stay")


			self.update(globalvars.GameSpeed)


			# Event handling
			for event in self.events():
				if event.type == pygame.QUIT:
					self.quit()
					return 0 
				if DrawButton.check(event):
					self.gamestate.dealToPlayer(my_player)
					self.gamestate.waitforplayer = False
				if StayButton.check(event):
					DrawButton.disable()
					my_player.stay(self.gamestate)
					self.gamestate.waitforplayer = False
				if ResolveButton.check(event):
					# end game when all players done and all cards revealed
					if all([not player.playing for player in self.gamestate.players]):
						if not self.gamestate.getFaceDowns():
							self.gamestate.endGame(reset = False)
							return 2	
						else:
							for card in self.gamestate.getFaceDowns():
								card.setFaceUp()
					self.gamestate.waitforplayer = False
				if ExitButton.check(event):
					self.gamestate.endGame()
					return 1

	def showPostgame(self):

		ExitButton = Button((30, 15), globalvars.StdFont, 30, globalvars.GREEN, "Quit", globalvars.YELLOW, globalvars.CYAN)
		self.gamestate.updateScore()

		while True:

			# Event handling
			for event in self.events():
				if event.type == pygame.QUIT:
					self.quit()
					return 0
				if ExitButton.check(event):
					return

			self.display.fill((255, 255, 255))

			for count, player in enumerate([player for player in self.gamestate.players if not player.isdealer]):
				self.vistext(Text((400,30*count), globalvars.StdFont,16,globalvars.BLACK),"{0} scored {1}".format(player.name, player.score))
			self.visbutton(ExitButton)
			self.update(globalvars.GameSpeed)


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

	def disable(self):
		"""disable button display and input"""
		self.state = False

	def enable(self):
		"""enables button diplay and input"""
		self.state = True

	def check(self,event):
		"""Returns True for a mouse click on the button"""

		if self.state:

			if event.type == MOUSEBUTTONUP:
				if self.position.collidepoint(event.pos):
					return True
		          
			if event.type == MOUSEMOTION or event.type == MOUSEBUTTONDOWN:
				if self.position.collidepoint(event.pos):
					self.surface = self.font.render(str(self.txt),True,self.colour,self.hover)
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
		radius = 250 # Radius of the display circle
		Woffset = 58 # Width co-ord adjustment
		Hoffset = 57 # Height co-ord adjustment
		areadist = 0 # How far in is the card area rendered
		self.locs = {}
		self.cardareas = {}

		for player in players:
			x = (radius * math.cos(radangle)) + (globalvars.WindowWidth / 2) - Woffset
			y = (radius * math.sin(radangle)) + (globalvars.WindowHeight / 2) - Hoffset

			coords = (x, y)
			self.locs[player] = coords
			player.loc = {"x" : x, "y" : y}

			#Card areas
			x = ((radius - areadist) * math.cos(radangle)) + (globalvars.WindowWidth / 2) - Woffset - 60
			y = ((radius - areadist) * math.sin(radangle)) + (globalvars.WindowHeight / 2) - Hoffset

			cardarea = PlayerArea(player, {"x" : x,"y" : y})
			player.cardarea = cardarea
			self.cardareas[player] = cardarea

			radangle += radian


class PlayerArea():
	def __init__(self, player, loc):
		self.player = player
		self.loc = loc

	def render(self, game):
		count = 1
		for card in self.player.getCards():
			img = card.img
			x = self.loc["x"] + (count * 30)
			y = self.loc["y"]
			cardloc = (x, y)
			if not card.faceup:
				img = globalvars.facedownimg
				
			game.vissurf(img, cardloc)
			count += 1

		return