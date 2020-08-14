# Game Controller module for applying game logic to the physics engine
from World import World
from config import *
from pygame.locals import (QUIT, KEYDOWN, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT)
from Box2D.b2 import polygonShape, dynamicBody
import numpy as np
from utils import Axis

class GameController:

	__instance__ = None

	def __init__(self):

		if not GameController.__instance__:
			
			self.PPM = PPM
			self.SCREEN_WIDTH = SCREEN_WIDTH
			self.SCREEN_HEIGHT = SCREEN_HEIGHT
			self.world = World.get_instance()

			self.__initialize_game_borders()
			self.__initialize_car()

			GameController.__instance__ = self

		else: 
			raise Exception("Game Controller already instanciated")

	def get_instance():

		if not GameController.__instance__:

			GameController.__instance__ = GameController()

		return GameController.__instance__

	def __initialize_game_borders(self):
		"""
		Builds borders for cointaning the game environment
		"""

		horizontal_width = self.SCREEN_WIDTH/self.PPM + 1
		vertical_height = self.SCREEN_HEIGHT/self.PPM + 1

		# Ground 
		ground = self.world.CreateStaticBody(position= (0, -1),shapes=polygonShape(box=(horizontal_width, 1)))
		
		# Left Wall
		left_wall = self.world.CreateStaticBody(position = (-1, 0), shapes = polygonShape(box= (1,vertical_height)))

		# Ceilling
		ceilling = self.world.CreateStaticBody(position = (0,vertical_height), shapes = polygonShape(box= (horizontal_width,1)))

		# Right Wall
		right_wall = self.world.CreateStaticBody(position = (horizontal_width,0), shapes = polygonShape(box= (1,vertical_height)))


	def __initialize_car(self):
		"""
		Initializes the car
		"""

		self.car = self.world.CreateDynamicBody(position=(10, 15))
		self.car.angularDamping = 0.1
		self.car_box = self.car.CreatePolygonFixture(box=(2, 1), density=1, friction=0.3)


	def update(self):
		"""
		Updates internal state of the game
		"""


