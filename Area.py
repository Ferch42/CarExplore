# Area class for plotting different terrains into the environment
from TerrainFactory import TerrainFactory

class Area:

	def __init__(self,lower_bound, upper_bound, terrain: str):

		self.lower_x, self.lower_y = lower_bound
		self.upper_x, self.upper_y = upper_bound
		self.terrain = TerrainFactory.get_terrain(str)

	def contains_point(self, point):
		"""
		Checks if a point is inside an Area
		"""
		x, y = point

		if (self.lower_x <= x) and (x <= self.upper_x) and (self.lower_y <= y) and (y <= self.upper_y):
			return True
		
		else:
			return False