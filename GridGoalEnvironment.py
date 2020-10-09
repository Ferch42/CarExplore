import numpy as np
import gym

class GridGoalEnvironment:

	def __init__(self, n = 10, holonomic = True, shuffle_goal = False, stochastic = False, radius = 1, discrete_goal = False):


		self.start_pos = (0,0)
		self.r = radius
		self.n = n
		self.goal = (n-self.r, n-self.r)
		self.shuffle_goal = shuffle_goal
		self.holonomic = holonomic
		self.stochastic = stochastic
		self.discrete_goal = discrete_goal
		self.n_actions = 2 if not self.holonomic else 4
		self.observation_n = 8 if not self.holonomic else 4
		self.observation_space = gym.spaces.Box(low = np.full(self.observation_n, 0), high = np.full(self.observation_n, n))
		self.action_space = gym.spaces.Discrete(self.n_actions)
		self.done = False
		self.orientation = 0
		self.timestep = 0
		self.max_timesteps = n**2

	def reshuffle_goal(self):

		new_position = self.new_goal()
		
		while(new_position[0] == self.pos[0] and new_position[1]== self.pos[1]):
			new_position = self.new_goal()
				
		self.goal = new_position


	def new_goal(self):

		new_position = (np.random.uniform()*self.n,np.random.uniform()*self.n)

		if self.discrete_goal:
			new_position = (int(new_position[0]), int(new_position[1]))

		return new_position
	
	def reset(self):

		self.pos = list(self.start_pos)	
		self.done = False
		self.timestep = 0
		
		if self.shuffle_goal:
			self.reshuffle_goal()

		return self.get_state()

	def get_state(self):

		return [self.pos[0], self.pos[1], self.goal[0], self.goal[1]] if self.holonomic else [self.pos[0], self.pos[1]]+ self.one_hot(self.orientation, 4) +  [self.goal[0], self.goal[1]]


	def one_hot(self, i, n):

		a = np.zeros(n)
		a[i] = 1
		return list(a)

	def get_reward(self):

		reached_goal = abs(self.pos[0]- self.goal[0])<= self.r and abs(self.pos[1]-self.goal[1])<=self.r
		return - int(not reached_goal)

	def step(self, action):

		if self.holonomic:

			self.apply_move(action)
		else:

			if action== 0:
				self.orientation = (self.orientation +1)%4
			
			if action==1:
				self.apply_move(self.orientation)

		r = self.get_reward()
		self.done = r == 0 or (self.timestep>= self.max_timesteps)
		self.timestep +=1
		return self.get_state(), r, self.done , {}


	def apply_move(self,move):

		if not self.stochastic:
				
			if move ==0:
				self.pos[0] = min(self.n, self.pos[0]+1)

			if move ==1:
				self.pos[0] = max(0, self.pos[0]-1)

			if move ==2:
				self.pos[1] = min(self.n, self.pos[1]+1)

			if move ==3:
				self.pos[1] = max(0, self.pos[1]-1)

		else:

			delta = np.random.normal(1,0.1)
			if move ==0:
				self.pos[0] = min(self.n, self.pos[0]+delta)

			if move ==1:
				self.pos[0] = max(0, self.pos[0]-delta)

			if move ==2:
				self.pos[1] = min(self.n, self.pos[1]+delta)

			if move ==3:
				self.pos[1] = max(0, self.pos[1]-delta)