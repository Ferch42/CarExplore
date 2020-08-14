# Area class for plotting different terrains into the environment
from TerrainFactory import TerrainFactory

class Area:

	def __init__(self,lower_bound, upper_bound, terrain: str):

		self.lower_x, self.lower_y = lower_bound
		self.upper_x, self.upper_y = upper_bound
		self.terrain = TerrainFactory.get_terrain(str)
