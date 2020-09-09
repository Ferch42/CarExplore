# Class Factory for retrieving Terrain Objects
from terrains.IceTerrain import IceTerrain
from terrains.AsphaltTerrain import AsphaltTerrain

class TerrainFactory:

	def get_terrain(terrain: str):
		
		return globals()[terrain]
