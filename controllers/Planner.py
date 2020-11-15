
import numpy as np
import tensorflow as tf

class Planner:


	def __init__(self, world_x, world_y, grid_size, actor, critic):

		self.world_x = world_x
		self.world_y = world_y
		self.grid_size = grid_size
		self.actor = actor
		self.critic = critic
		self.grid = np.full((int(self.world_x/self.grid_size), int(self.world_y/self.grid_size)), False, dtype = bool)


	def get_action(self,state):

		s = list(state)
		self.update_internal_state(state)

		options = self.get_options()
		actions  = []
		critic_values = []

		for o in options:
			S = tf.expand_dims(tf.convert_to_tensor(s+o), 0)
			action = self.actor(S)
			actions.append(tf.squeeze(action))
			critic_values.append(self.critic(S, action))


		return actions[np.argmax(critic_values)]



	def update_internal_state(self,state);

		x, y = int(state[0]/self.grid_size), int(state[1]/self.grid_size)
		self.grid[x][y] = True

	def get_options(self):

		options = []
		width, length = self.grid.shape

		for w in range(width):
			for l in range(length):
				if not self.grid[w][l]:
					options.append([w*self.grid_size + self.grid_size/2, l*self.grid_size + self.grid_size/2])

		return options