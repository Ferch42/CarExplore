# GOAL FINDING ENVIRONMENT

from controllers.GameController import GameController
from controllers.Area import Area
import numpy as np

class GoalController(GameController):

	def __init__(self):

		super().__init__()
		self.__GOAL_pos = (30,30)
		self.__GOAL_found = False
		self.__GOAL_radius = 1
		self._obstacles_areas = self._get_obstacles_areas()


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

	def _get_obstacles_areas(self):
		"""
		Get obstacle areas where the GOAL cannot spawn
		"""
		areas = []

		for o in self.obstacles:
			min_x, min_y = 0,0
			max_x, max_y = 0,0

			for x,y in o:
				min_x = min(x, min_x)
				min_y = min(y, min_y)
				max_x = max(x, max_x)
				max_y = max(y, max_y)

			areas.append(Area((min_x-self.__GOAL_radius,min_y-self.__GOAL_radius), (max_x+self.__GOAL_radius,max_y+self.__GOAL_radius)))

		return areas

	def _valid_GOAL_point(self, point):
		"""
		Checks if a point is valid to be spawn given the obstacles
		"""
		flag = True

		for a in self._obstacles_areas:
			flag = flag and (not a.contains_point(point))

		return flag

	def _reset_GOAL(self):

		x,y = self._choose_random_GOAL_points()

		while(not self._valid_GOAL_point((x,y))):
			
			x,y = self._choose_random_GOAL_points()

		self.__GOAL_pos = (x,y)
		self.__GOAL_found = False


	def _choose_random_GOAL_points(self):

		x = np.random.randint(self.__GOAL_radius, self.WORLD_WIDTH+1-self.__GOAL_radius)	
		y = np.random.randint(self.__GOAL_radius, self.WORLD_HEIGHT+1-self.__GOAL_radius)

		return x,y