# Area class for plotting different terrains into the environment
from terrains.TerrainFactory import TerrainFactory

class Area:

	def __init__(self,lower_bound, upper_bound, terrain= None):

		self.lower_x, self.lower_y = lower_bound
		self.upper_x, self.upper_y = upper_bound
		
		if terrain is not None:
			self.terrain = TerrainFactory.get_terrain(terrain)

	def contains_point(self, point):
		"""
		Checks if a point is inside an Area
		"""
		x, y = point

		if (self.lower_x <= x) and (x <= self.upper_x) and (self.lower_y <= y) and (y <= self.upper_y):
			return True
		
		else:
			return False