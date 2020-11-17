# GOAL ENVIRONMENT 

import gym
from controllers.SweepController import SweepController
from views.SweepInterface import SweepInterface
import numpy as np

class GridEnvironment(gym.Env):

	metadata = {"render.modes": ['human']}

	def __init__(self, max_timesteps = 1000):

		self.controller = SweepController()
		self.interface = SweepInterface()
		self.interface.set_controller(self.controller)
		self.observation_space_n = 6
		self.observation_space = gym.spaces.Box(low = np.full(self.observation_space_n, -np.inf), high = np.full(self.observation_space_n, np.inf))
		self.max_acceleration = 100
		self.max_torque = 100
		self.action_space = gym.spaces.Box(low = np.array([-self.max_acceleration, -self.max_torque]), high = np.array([self.max_acceleration, self.max_torque]))
		self.reward = -1
		self.done = False
		self.max_timesteps = max_timesteps
		self.timestep = 1


	def step(self, action):

		#starting_position = self.controller.get_car_state()
		#car_start_x, car_start_y = starting_position[0], starting_position[1]
		
		self.controller.update()
		#self.controller.handle_event(action)
		ac, tor = action
		ac = np.clip(ac, -self.max_acceleration, self.max_acceleration)*50
		tor = np.clip(tor, -self.max_torque, self.max_torque)*5

		self.controller.apply_acceleration(ac)
		self.controller.apply_torque(tor)

		self.controller.step()

		self.done = self.controller.get_grid_done() or (self.timestep >= self.max_timesteps)
		self.timestep+=1
	
		return self._get_observation(), self.reward, self.done , {}

	def reset(self):

		self.controller.reset()
		self.timestep = 0
		return self._get_observation()

	def _get_observation(self):
		"""
		Gets the observation vector for the agent
		"""
		observation = self.controller.get_car_state()
		
		return np.array(observation)


	def render(self, mode ='human'):

		self.interface.render()

	def close(self):

		self.interface.quit()


