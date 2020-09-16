# Class resposible for dealing with rendering
from utils.Singleton import Singleton
from config import *
import pygame
from pygame.locals import (QUIT, KEYDOWN, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT)
from enums.Body import Body
from controllers.GameController import GameController

class Interface(metaclass = Singleton):


	def __init__(self):

		# The Controller needs to be set by the ApplicationFactory
		self.controller = None
		# Pygame setup
		self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		pygame.display.set_caption('CarExplore')
		#self.clock = pygame.time.Clock()
		self.TARGET_FPS = TARGET_FPS
		# body colours
		self.colors = {
		Body.STATIC: (0, 0, 0, 255),
		Body.DYNAMIC: (255, 165, 0, 255)}


	def set_controller(self, controller):
		"""
		Setter for the controller
		"""
		self.controller = controller

	def render(self):
		"""
		Renders all the information about the game
		"""
		self._render_background()
		self._render_terrains()
		self._render_bodies()
		self._flip()
		
		
	def _flip(self):
		"""
		Flips in pygame
		"""
		pygame.display.flip()
		#self.clock.tick(self.TARGET_FPS)
	
	def _render_background(self):
		"""
		Renders the background terrain
		"""
		self.screen.fill(self.controller.get_default_terrain_color())

	def _render_terrains(self):
		"""
		Renders the custom terrains
		"""
		
		terrains = self.controller.get_terrains()

		for terrain in terrains:

			t_color = terrain['COLOR']
			rect_dim = terrain['RECT']
			pygame.draw.rect(self.screen,t_color, rect_dim)

	def _render_bodies(self):
		"""
		Renders the custom terrains
		"""
		
		bodies = self.controller.get_bodies()

		for b in bodies:

			body_type = b["BODY"]
			vertices = b["VERTICES"]
			pygame.draw.polygon(self.screen, self.colors[body_type], vertices)

	def quit(self):
		"""
		Exits interface
		"""

		pygame.quit()