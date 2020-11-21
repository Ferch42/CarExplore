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
		self.observation_space_n = 8
		self.observation_space = gym.spaces.Box(low = np.full(self.observation_space_n, -np.inf), high = np.full(self.observation_space_n, np.inf))
		self.max_acceleration = 100
		self.max_torque = 100
		self.action_space = gym.spaces.Box(low = np.array([-self.max_acceleration, -self.max_torque]), high = np.array([self.max_acceleration, self.max_torque]))
		self.reward = -1
		self.done = False
		self.max_timesteps = max_timesteps
		self.timestep = 1
		self.random_GOAL = random_GOAL
		self.max_length = np.sqrt(self.controller.WORLD_WIDTH**2 + self.controller.WORLD_HEIGHT**2) 

	def step(self, action):

		#starting_position = self.controller.get_car_state()
		#car_start_x, car_start_y = starting_position[0], starting_position[1]
		
		self.controller.update()
		#self.controller.handle_event(action)
		ac, tor = action
		ac = np.clip(ac, -self.max_acceleration, self.max_acceleration)*100
		tor = np.clip(tor, -self.max_torque, self.max_torque)*5

		self.controller.apply_acceleration(ac)
		self.controller.apply_torque(tor)

		self.controller.step()

		self.done = self.controller.get_GOAL_found() or (self.timestep >= self.max_timesteps)
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
		GOAL_x, GOAL_y = self.controller.get_GOAL_pos()

		if self.random_GOAL or True:
			observation = observation+[GOAL_x, GOAL_y]

		return np.array(observation)


	def render(self, mode ='human'):

		self.interface.render()

	def close(self):

		self.interface.quit()

	def get_reward(self):

		observation  = self.controller.get_car_state()
		x_car, y_car = observation[0], observation[1]
		GOAL_x, GOAL_y = self.controller.get_GOAL_pos()
		
		dist = np.sqrt((x_car-GOAL_x)**2+ (y_car- GOAL_y)**2)

		return -dist
