# GOAL ENVIRONMENT 

import gym
from controllers.GoalController import GoalController
from views.GoalInterface import GoalInterface
import numpy as np

class GoalEnvironment(gym.Env):

	metadata = {"render.modes": ['human']}

	def __init__(self, random_GOAL = False, max_timesteps = 200):

		self.controller = GoalController(random_GOAL = random_GOAL)
		self.interface = GoalInterface()
		self.interface.set_controller(self.controller)
		self.observation_space_n = 5 if not random_GOAL else 7
		self.observation_space = gym.spaces.Box(low = np.full(self.observation_space_n, -np.inf), high = np.full(self.observation_space_n, np.inf))
		self.action_space = gym.spaces.Discrete(5)
		self.reward = -1
		self.done = False
		self.max_timesteps = max_timesteps
		self.timestep = 1
		self.random_GOAL = random_GOAL

	def step(self, action):

		self.controller.update()
		self.controller.handle_event(action)
		self.controller.step()
		self.done = self.controller.get_GOAL_found() or (self.timestep >= self.max_timesteps)
		self.timestep+=1

		return self._get_status()

	def reset(self):

		self.controller.reset()
		self.timestep = 0
		return self._get_status()[0]

	def _get_observation(self):
		"""
		Gets the observation vector for the agent
		"""
		observation = self.controller.get_car_state()
		GOAL_x, GOAL_y = self.controller.get_GOAL_pos()

		if self.random_GOAL:
			observation = observation+[GOAL_x, GOAL_y]

		return np.array(observation)

	def _get_status(self):
		"""
		Gets the status to be returned by the environment
		"""
		return self._get_observation(), self.reward, self.done , None


	def render(self, mode ='human'):

		self.interface.render()

	def close(self):

		self.interface.quit()

	def get_reward(self):

		x_car, y_car, _,_,_ = self.controller.get_car_state()
		GOAL_x, GOAL_y = self.controller.get_GOAL_pos()
		
		dist = np.sqrt((x_car-GOAL_x)**2+ (y_car- GOAL_y)**2)

		return -dist
