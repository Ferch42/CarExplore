# Class resposible for dealing with rendering
from utils.Singleton import Singleton
from config import *
import pygame
from pygame.locals import (QUIT, KEYDOWN, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT)
from enums.Body import Body
from controllers.GameController import GameController

class Interface(metaclass = Singleton):


	def __init__(self):

		# Controller
		self.controller = GameController()
		# Pygame setup
		self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		pygame.display.set_caption('CarExplore')
		self.clock = pygame.time.Clock()
		self.TARGET_FPS = TARGET_FPS
		# body colours
		self.colors = {
		Body.STATIC: (0, 0, 0, 255),
		Body.DYNAMIC: (255, 165, 0, 255)}


	def render(self):
		"""
		Renders all the information about the game
		"""
		self.__render_background()
		self.__render_terrains()
		self.__render_bodies()
		
		pygame.display.flip()
		self.clock.tick(TARGET_FPS)
	

	def __render_background(self):
		"""
		Renders the background terrain
		"""
		self.screen.fill(self.controller.get_default_terrain_color())

	def __render_terrains(self):
		"""
		Renders the custom terrains
		"""
		
		terrains = self.controller.get_terrains()

		for t in terrains:

			t_color, rect_dim = t
			pygame.draw.rect(self.screen,t_color, rect_dim)

	def __render_bodies(self):
		"""
		Renders the custom terrains
		"""
		
		bodies = self.controller.get_bodies()

		for b in bodies:

			body_type, vertices = b
			pygame.draw.polygon(self.screen, self.colors[body_type], vertices)

	def quit(self):
		"""
		Exits interface
		"""

		pygame.quit()