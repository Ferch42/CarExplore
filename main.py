from GoalEnvironment import GoalEnvironment
import numpy as np
import random
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam


# Hyperparameters
max_timesteps = 10000
episodes = 10000
initial_episilon = 1
episilon = 0.1
exploration_linear_decay = 0.00001
gamma = 0.99
batch_size = 32
lr = 0.001
C = 10000
replay_buffer_size = 1000000

# Variables
env = GoalEnvironment()
replay_buffer = list()
timestep = 0

# Model definition and clonning
Q_net = Sequential()
Q_net.add(Dense(32, input_shape = env.observation_space.shape, activation = 'relu'))
Q_net.add(Dense(32, activation = 'relu'))
Q_net.add(Dense(32, activation = 'relu'))
Q_net.add(Dense(env.action_space.n))
print(Q_net.summary())

Q_target_net = keras.models.clone_model(Q_net)
Q_target_net.set_weights(Q_net.get_weights()) 

# Model compiling 
Q_net.compile(loss = 'mse', optimizer = Adam(learning_rate = lr))
Q_target_net.compile(loss = 'mse', optimizer = Adam(learning_rate = lr))

# Helper functions
def get_episilon_greedy_action(state,e= episilon):
	global Q_net, episilon

	p = np.random.uniform()
	
	if p<= episilon:
		return np.random.randint(env.action_space.n)
	else:
		Q = Q_net.predict(np.array([state]))[0]
		return Q.argmax()


def extract(l, i):

	return [x[i] for x in l]

def train():

	global Q_net, Q_target_net, replay_buffer, gamma

	batch = random.sample(replay_buffer, batch_size)

	states = np.array(extract(batch, 0))
	actions = np.array(extract(batch,1))
	rewards = np.array(extract(batch,2))
	next_states = np.array(extract(batch,3))
	dones = extract(batch, 4)

	Q_target = Q_target_net.predict(np.array(next_states))
	
	for i in range(batch_size):
		target = rewards[i]
		
		if not dones[i]:
			target = target + gamma*Q_target[i].max()

		Q_target[i][actions[i]] = target

	Q_net.fit(states, Q_target, verbose = False)

def add_transition(transition):

	global replay_buffer, replay_buffer_size
	
	replay_buffer.append(transition)
	replay_buffer = replay_buffer[-replay_buffer_size:]

for i_episode in range(episodes):
	s = env.reset()

	for t in range(max_timesteps):
		#env.render()
		a = get_episilon_greedy_action(s, e= min(initial_episilon - exploration_linear_decay*timestep, episilon))
		ss, r, done, info = env.step(a)
		add_transition((s,a,r,ss, done))
		
		if len(replay_buffer) > batch_size:
			train()

		if timestep%C ==0:
			Q_target_net.set_weights(Q_net.get_weights()) 

		timestep += 1

		if done:

			print("Episode", i_episode," done in ", t, " timesteps")
			break
env.close()
