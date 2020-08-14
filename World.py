# Singleton model for containing the Box2d world
from Box2D.b2 import world

class World:
	
	__instance__ = None

	def get_instance():

		if not World.__instance__:
			World.__instance__ = world(gravity=(0, 0), doSleep=True)

		return World.__instance__