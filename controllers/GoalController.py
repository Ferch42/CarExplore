# GOAL FINDING ENVIRONMENT

from controllers.GameController import GameController
from controllers.Area import Area
import numpy as np

class GoalController(GameController):

	def __init__(self, random_GOAL = False):

		super().__init__()
		self.__GOAL_found = False
		self.__GOAL_radius = 1
		self.__GOAL_diameter = 4*self.__GOAL_radius
		self.__GOAL_pos = (int(self.WORLD_WIDTH-self.__GOAL_diameter),int(self.WORLD_HEIGHT-self.__GOAL_diameter))
		self._obstacles_areas = self._get_obstacles_areas()
		self.random_GOAL = random_GOAL

		if random_GOAL:
			self._reset_GOAL()

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

		return {'GOAL_center': (int(goal_render_pos_x), int(goal_render_pos_y)), 'GOAL_found': self.__GOAL_found, 'GOAL_radius':self.__GOAL_radius*self.PPM}

	def update(self):
		"""
		Overwritting update method
		"""
		super().update()
		if self.car_reached_goal():

			self.__GOAL_found = True
			#self._reset_GOAL()
	
	def get_GOAL_pos(self):
		"""
		GOAL pos getter
		"""
		return self.__GOAL_pos

	def get_GOAL_found(self):
		"""
		GOAL found getter
		"""
		return self.__GOAL_found

	def reset(self):
		"""
		Resets environment
		"""
		car_pos = self._choose_random_GOAL_points()
		self._reset_car(car_pos)
		self.__GOAL_found = False
		if self.random_GOAL:
			self._reset_GOAL()


	def _get_obstacles_areas(self):
		"""
		Get obstacle areas where the GOAL cannot spawn
		"""
		areas = []

		for o in self.obstacles:
			min_x, min_y = np.inf,np.inf
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
		"""
		Resets the GOAL to a new random position
		"""
		x,y = self._choose_random_GOAL_points()

		while not self._valid_GOAL_point((x,y)):
			
			x,y = self._choose_random_GOAL_points()

		self.__GOAL_pos = (x,y)


	def _choose_random_GOAL_points(self):

		x = np.random.uniform(self.__GOAL_diameter, self.WORLD_WIDTH-self.__GOAL_diameter)	
		y = np.random.uniform(self.__GOAL_diameter, self.WORLD_HEIGHT-self.__GOAL_diameter)

		return x,y