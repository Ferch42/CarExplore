# Singleton model for containing the Box2d world
from utils.Singleton import Singleton
from Box2D.b2 import world

class World(metaclass = Singleton):
	
	def __init__(self):

		self.world =world(gravity=(0, 0), doSleep=True)

	def get_world(self):
		
		return self.world