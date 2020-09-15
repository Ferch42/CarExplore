# GOAL FINDING ENVIRONMENT INTERFACE RENDERER

from views.Interface import Interface
import pygame

class GoalInterface(Interface):

	def __init__(self):

		super().__init__()
		self.__GOAL_FOUND_COLORS = {
		False: (255,255,0,255),
		True: (50, 205, 50, 255)  
		}



	def render(self):
		"""
		Overwritting render method all the information about the game
		"""
		super()._render_background()
		super()._render_terrains()
		self._render_GOAL()
		super()._render_bodies()
		self._flip()

	def _render_GOAL(self):
		"""
		Draws the GOAL in the screen
		"""

		GOAL_info = self.controller.get_goal_render_stats()
		pygame.draw.circle(self.screen, self.__GOAL_FOUND_COLORS[GOAL_info['GOAL_found']], GOAL_info['GOAL_center'], GOAL_info['GOAL_radius'])
