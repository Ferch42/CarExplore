from GoalEnvironment import GoalEnvironment
import numpy as np

env = GoalEnvironment(True)


class OUActionNoise:
	def __init__(self, mean, std_deviation, theta=0.15, dt=1e-2, x_initial=None):
		self.theta = theta
		self.mean = mean
		self.std_dev = std_deviation
		self.dt = dt
		self.x_initial = x_initial
		self.reset()

	def __call__(self):
		# Formula taken from https://www.wikipedia.org/wiki/Ornstein-Uhlenbeck_process.
		x = (
			self.x_prev
			+ self.theta * (self.mean - self.x_prev) * self.dt
			+ self.std_dev * np.sqrt(self.dt) * np.random.normal(size=self.mean.shape)
		)
		# Store x into x_prev
		# Makes next noise dependent on current one
		self.x_prev = x
		return x

	def reset(self):
		if self.x_initial is not None:
			self.x_prev = self.x_initial
		else:
			self.x_prev = np.zeros_like(self.mean)

std_dev = 1


ou_noise = OUActionNoise(mean=np.zeros(2), std_deviation=float(std_dev) * np.ones(2))

for i in range(10000):
	
	env.reset()
	print(i)
	while(True):

		env.render()
		a = ou_noise()
		print(a)
		ss, r, done, info = env.step(a)	

		if done:
			break