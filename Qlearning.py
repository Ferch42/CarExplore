
from GridGoalEnvironment import GridGoalEnvironment
import numpy as np
import random

# hyperparameters
number_of_episodes = 1000000
episilon = 0.1
learning_rate = 0.1
replay_buffer_size = 1
batch_size = 32
gamma = 0.99
max_timesteps = 100000
mean_proportion = 0.1

discrete = lambda x: np.array([int(z) for z in x])

def insert_state(state, Q):

	if state not in Q.keys():
		Q[state] = np.zeros(env.action_space.n)



env = GridGoalEnvironment(n = 10,shuffle_goal = True, discrete_goal = True, stochastic = True, holonomic = False)
Q = dict()
replay_buffer = list()
rewards = list()
running_reward = 0
timestep = 0

def episilon_greedy(state, e = episilon):

	global Q
	insert_state(state, Q)
	p = np.random.uniform()

	if p<=e:

		return np.random.randint(env.action_space.n)
	
	else:

		Q_max = Q[state].max()
		max_indexes = [x for x in range(env.action_space.n) if Q[state][x]==Q_max]

		return random.choice(max_indexes)


def add_transition(transition):

	global replay_buffer, replay_buffer_size
	
	replay_buffer.append(transition)

	if len(replay_buffer)>replay_buffer_size:
		del replay_buffer[:1]
		
def train():

	global replay_buffer, Q, replay_buffer_size

	#for exp in random.sample(replay_buffer, min(len(replay_buffer), batch_size)):
	for exp in replay_buffer:
		s,a,r,ss,done = exp
		insert_state(ss, Q)
		td_error = r + gamma*Q[ss].max() - Q[s][a]
		Q[s][a] = Q[s][a] + learning_rate*td_error

for ep in range(number_of_episodes):

	s = env.reset()
	s = str(discrete(s))
	cumulative_reward = 0
	for i in range(max_timesteps):

		a = episilon_greedy(s, e = episilon)
		ss, r, done, _ = env.step(a)
		ss = str(discrete(ss))

		experience = (s,a,r,ss,done)
		add_transition(experience)
		train()
		cumulative_reward+=r
		s = ss
		timestep+=1

		if timestep % 10000==0:
			print('Number of episodes done: ', ep)
			print('running_reward :', running_reward)
			print('Mean reward: ', np.array(rewards).mean())
			#print(Q)

		if done:
			#print(cumulative_reward)
			rewards.append(cumulative_reward)
			running_reward = running_reward*(1-mean_proportion) + mean_proportion *cumulative_reward
			break
