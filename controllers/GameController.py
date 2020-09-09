# Game Controller module for applying game logic to the physics engine
from utils.Singleton import Singleton
from models.World import World
from config import *
from pygame.locals import (QUIT, KEYDOWN, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT)
from Box2D.b2 import polygonShape, dynamicBody
from utils.car_explore_utils import deserialize_areas, deserialize_obstacles
from terrains.TerrainFactory import TerrainFactory
from enums.Body import Body
from events.EventFactory import EventFactory

class GameController(metaclass= Singleton):


	def __init__(self):
			
		self.PPM = PPM
		self.SCREEN_WIDTH = SCREEN_WIDTH
		self.SCREEN_HEIGHT = SCREEN_HEIGHT
		self.TIME_STEP = TIME_STEP
		self.world = World().get_world()

		self.__initialize_game_borders()
		self.__initialize_car()

		self.areas = deserialize_areas()
		self.default_terrain = 'AsphaltTerrain'
		self.terrain = TerrainFactory.get_terrain(self.default_terrain)

		self.__build_obstacles()



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
		
		self.terrain = TerrainFactory.get_terrain(self.default_terrain)
		for a in self.areas:
			if a.contains_point(self.car.worldCenter):
				self.terrain = a.terrain

		self.terrain.apply_ordinary_forces(self.car)

	def handle_event(self, event):
		"""
		Handles input commands
		"""
		self.terrain.handle_impulse_event(self.car, EventFactory.create(event))

	def get_default_terrain_color(self):
		"""
		Returns the default terrain colour
		"""
		return TerrainFactory.get_terrain(self.default_terrain).COLOR

	def get_terrains(self):
		"""
		Returns the areas of different terrains and their colors for the UI to render (the returned value is specially adapted for the pygame engine)
		The returned value is a list of tuples of the type [(colour, [rect_information])]
		"""

		render_areas = []

		for a in self.areas:

			a_color = a.terrain.COLOR
			rect_width = (a.upper_x - a.lower_x)*self.PPM
			rect_height = (a.upper_y - a.lower_y)*self.PPM
			lower_x = a.lower_x*self.PPM
			lower_y = self.SCREEN_HEIGHT - a.lower_y*self.PPM - rect_height

			render_areas.append((a_color, [lower_x, lower_y, rect_width,rect_height]))

		return render_areas

	def get_bodies(self):
		"""
		Returns the objects and their coordinates
		"""
		fixtures = []

		for body in self.world.bodies:

			for fixture in body.fixtures:
				
				shape = fixture.shape
				vertices = [(body.transform * v) * self.PPM for v in shape.vertices]
				vertices = [(v[0], self.SCREEN_HEIGHT - v[1]) for v in vertices]
				
				fixtures.append((Body(body.type), vertices))

		return fixtures

	def step(self):

		self.world.Step(self.TIME_STEP, 10, 10)

	def __build_obstacles(self):
		"""
		Builds the obstacles for the game
		"""

		obstacles = deserialize_obstacles()
		
		for o_vertices in obstacles:
			self.world.CreateStaticBody(shapes=polygonShape(vertices=o_vertices))