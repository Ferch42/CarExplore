# GOAL FINDING ENVIRONMENT

from controllers.GameController import GameController
import numpy as np

class GoalController(GameController):

	def __init__(self):

		super().__init__()
		self.__GOAL_pos = (30,30)
		self.__GOAL_found = False
		self.__GOAL_radius = 1


	def car_reached_goal(self):
		"""
		Checks if car has reached the goal
		"""
		car_x, car_y = self.car.worldCenter
		goal_x, goal_y = self.__GOAL_pos

		distance = np.sqrt((car_x- goal_x)**2 + (car_y -goal_y)**2)

		return distance<= self.__GOAL_radius

	def get_goal_render_stats(self):
		"""
		Returns render GOAL information to the interface
		"""

		goal_x, goal_y = self.__GOAL_pos
		goal_render_pos_x, goal_render_pos_y = self.PPM * goal_x , self.SCREEN_HEIGHT - self.PPM * goal_y

		return {'GOAL_center': (goal_render_pos_x, goal_render_pos_y), 'GOAL_found': self.__GOAL_found, 'GOAL_radius':self.__GOAL_radius*self.PPM}

	def update(self):
		"""
		Overwritting update method
		"""
		super().update()
		if self.car_reached_goal():

			self.__GOAL_found = True