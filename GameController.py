# Game Controller module for applying game logic to the physics engine
from World import World
from config import *
from pygame.locals import (QUIT, KEYDOWN, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT)
from Box2D.b2 import polygonShape, dynamicBody
import os
import Area
from utils import *
from TerrainFactory import TerrainFactory

class GameController:

	__instance__ = None

	def __init__(self):

		if not GameController.__instance__:
			
			self.PPM = PPM
			self.SCREEN_WIDTH = SCREEN_WIDTH
			self.SCREEN_HEIGHT = SCREEN_HEIGHT
			self.TIME_STEP = TIME_STEP
 			self.world = World.get_instance()

			self.__initialize_game_borders()
			self.__initialize_car()

			self.areas = deserialize_areas()
			self.default_terrain = 'AsphaltTerrain'
			self.terrain = TerrainFactory.get_terrain(self.default_terrain)

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
		
		# Check terrain of the area
		
		for a in self.areas:
			if a.contains_point(self.car.worldCenter):
				self.terrain = a.terrain

		self.terrain.apply_ordinary_forces(self.car)

	def handle_event(self, event):
		"""
		Handles input commands
		"""
		self.terrain.handle_impulse_event(self.car, event)

	def get_default_terrain_color(self):
		"""
		Returns the default terrain colour
		"""
		return TerrainFactory.get_terrain(self.default_terrain).COLOR

	def get_areas(self):
		"""
		Returns the areas of different terrains and their colors for the UI to render (the returned value is specially adapted for the pygame engine)
		The returned value is a list of tuples of the type [(colour, [rect_information])]
		"""

		render_areas = []

		for a in self.areas:

			a_color = a.COLOR
			lower_x = a.lower_x
			lower_y = self.SCREEN_HEIGHT - a.lower_y
			rect_width = a.upper_x - a.lower_x
			rect_height = a.upper_y - a.lower_y

			render_areas.append((a_color, [lower_x, lower_y, rect_width,rect_height]))

		return render_areas

	def get_objects(self):
		"""
		Returns the objects and their coordinates
		"""
		fixtures = []

		for body in world.bodies:

			for fixture in body.fixtures:
				
				shape = fixture.shape
				vertices = [(body.transform * v) * self.PPM for v in shape.vertices]
				vertices = [(v[0], self.SCREEN_HEIGHT - v[1]) for v in vertices]
				
				fixtures.append((Body(body.type), vertices))

		return fixtures

	def step(self):

		self.world.Step(self.TIME_STEP, 10, 10)