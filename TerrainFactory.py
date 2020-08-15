# Class Factory for retrieving Terrain Objects
from IceTerrain import IceTerrain
from AsphaltTerrain import AsphaltTerrain

class TerrainFactory:

	def get_terrain(terrain: str):
		
		return globals()[terrain]
