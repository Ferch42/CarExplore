from views.Interface import Interface
import pygame


class SweepInterface(Interface):

	def __init__(self):

		super().__init__()
		self.__GRID_COLOUR = (255,255,255,255)
		self.__GOAL_OCCUPATION_COLORS = {
		False: (204,0,0,255),
		True: (50, 205, 50, 255)  
		}

	def _render_grid(self):
		"""
		Renders exploration grid
		"""	
		lines = self.controller.get_grid_lines()

		for line in lines:

			start_pos, end_pos = line 
			pygame.draw.line(self.screen, self.__GRID_COLOUR, start_pos, end_pos)


	def _render_occupancy_squares(self):
		"""
		Renders occupancy squares
		"""
		squares = self.controller.get_occupancy_squares()

		for square in squares:

			pygame.draw.rect(self.screen, self.__GOAL_OCCUPATION_COLORS[square["OCCUPANCY"]], square["RECT"])



	def render(self):
		"""
		Overwritting render method all the information about the game
		"""
		super()._render_background()
		super()._render_terrains()
		self._render_grid()
		self._render_occupancy_squares()
		super()._render_bodies()
		self._flip()
