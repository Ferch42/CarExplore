# Singleton model for containing the Box2d world

from Singleton import Singleton
from Box2D.b2 import world

class World(Singleton):
	
	def __init__(self):

		self = world(gravity=(0, 0), doSleep=True)