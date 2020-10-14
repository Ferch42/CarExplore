from GoalEnvironment import GoalEnvironment
from GridGoalEnvironment import GridGoalEnvironment
import numpy as np
import gym
import random
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam, RMSprop
from matplotlib import pyplot as plt
import tensorflow as tf
import pickle
from time import time
from datetime import timedelta
from sklearn.preprocessing import StandardScaler
from prioritized_memory import Memory


# Hyperparameters
max_timesteps = 1000000
episodes = 1000000
random_steps = 50000
initial_episilon = 1
episilon = 0.1
update_frequency = 1
exploration_annealing_frames = 1000000
gamma = 0.99
batch_size = 32
lr = 0.00001
C = 10000
clip_norm = 1
replay_buffer_size = 100000
DOUBLE_DQN = True
load_weights = False
average_proportion = 0.01
OPT = Adam
Hindsight_experience_replay = True

# Variables
env = GoalEnvironment(random_GOAL = True)
#env = gym.make('Acrobot-v1')
#env = GridGoalEnvironment(n = 10,shuffle_goal = True, discrete_goal = True, stochastic = True, holonomic = False)

replay_buffer = Memory(replay_buffer_size)
#replay_buffer = list()
timestep = 0
episode_timestep_history = list()
reward_history = list()
C = C *update_frequency
exploration_linear_decay = 1/exploration_annealing_frames
running_reward = 0
scaler = StandardScaler()
min_reward = - 1/(1-gamma)
temporal_diff_mean = 0
update_count = 0

# Model definition and clonning
Q_net = Sequential()
Q_net.add(Dense(64, input_shape = env.observation_space.shape, activation = 'relu'))
Q_net.add(Dense(64, activation = 'relu'))
Q_net.add(Dense(64, activation = 'relu'))
Q_net.add(Dense(env.action_space.n, activation= 'linear'))
print(Q_net.summary())

#assert(not load_weights)
#assert( DOUBLE_DQN)

if load_weights:
	print("LOADED WEIGHTS")
	Q_net.load_weights("DQN.h5")

Q_target_net = keras.models.clone_model(Q_net)
Q_target_net.set_weights(Q_net.get_weights()) 

# Model compiling 
Q_net.compile(loss = "mse", optimizer = OPT(learning_rate = lr, clipnorm = clip_norm))
Q_target_net.compile(loss = "mse", optimizer = OPT(learning_rate = lr, clipnorm = clip_norm))


#ower_normalized_bound = np.full(env.observation_space.shape, -5)
#per_normalized_bound = np.full( env.observation_space.shape, 5)

# Helper functions
def normalize(states):

	global scaler
	scaler.partial_fit(states)

	return scaler.transform(states)

def get_episilon_greedy_action(state,e):
	global Q_net

	p = np.random.uniform()
	
	if p<= e:
		return np.random.randint(env.action_space.n)
	else:
		s = normalize(np.array([state]))
		Q = Q_net.predict(s)[0]
		return Q.argmax()


def get_reward1(s,a,ss, g, episilon = 1):

	ss_x,ss_y = ss[0:2]
	g_x, g_y = g
	dist = np.sqrt((ss_x-g_x)**2 + (ss_y- g_y)**2)
	
	return -int(dist > episilon)

def get_reward2(s,a,ss,g,episilon = 1):

	reached_goal = abs(ss[0]- g[0])<= episilon and abs(ss[1]-g[1])<=episilon
	
	return - int(not reached_goal)

def plot_episode_lenght_history():

	global episode_timestep_history

	plt.title("EPISODE LENGHT HISTORY")
	plt.plot(range(len(episode_timestep_history)), episode_timestep_history)
	plt.plot(range(len(episode_timestep_history)), smooth(episode_timestep_history))
	plt.savefig("EpisodeLenght.png")
	plt.clf()

def plot_reward_history():

	global reward_history

	plt.title("Reward HISTORY")
	plt.plot(range(len(reward_history)), reward_history)
	plt.plot(range(len(reward_history)), smooth(reward_history))
	plt.savefig("Reward.png")
	plt.clf()


def smooth(l, smooth_interval = 1000):

	if len(l)==0:
		return l

	npl = np.array(l)
	smoothed_list = np.zeros(len(l))
	smoothed_list[0] = npl[0]
	for i in range(1,len(l)):
		smoothed_list[i] = npl[max((i-smooth_interval),0):i].mean()

	return smoothed_list


def extract(l, i):

	return [x[i] for x in l]

def train():

	global Q_net, Q_target_net, replay_buffer, gamma, temporal_diff_mean

	#batch = random.sample(replay_buffer, batch_size)
	batch, idxs, IS_weights = replay_buffer.sample(batch_size)

	states = np.array(extract(batch, 0))
	actions = np.array(extract(batch,1))
	rewards = np.array(extract(batch,2))
	next_states = np.array(extract(batch,3))

	states = normalize(states)
	next_states = normalize(next_states)

	dones = extract(batch, 4)

	Q_next = Q_target_net.predict(next_states)
	Q_target = Q_net.predict(states)

	tds = []
	if not DOUBLE_DQN:

		for i in range(batch_size):
			target = rewards[i]
			
			if not dones[i]:
				target = target + gamma*Q_next[i].max()

			target = np.clip(target, min_reward, 0)
			td = target - Q_target[i][actions[i]]
			tds.append(td)
			Q_target[i][actions[i]] = target
	
	else:

		Q_next_2 = Q_net.predict(next_states)
		
		for i in range(batch_size):
			target = rewards[i]

			if not dones[i]:
				target = target + gamma* Q_next[i][Q_next_2[i].argmax()]

			target = np.clip(target, min_reward, 0)
			td = target - Q_target[i][actions[i]] 
			tds.append(td)
			Q_target[i][actions[i]] = target
	

	tds = np.abs(tds)
	temporal_diff_mean = temporal_diff_mean*(1- average_proportion) + average_proportion *tds.mean()
	
	Q_net.fit(states, Q_target, verbose = False, sample_weight = np.array(IS_weights))

	for idx, td in zip(idxs, tds):
		replay_buffer.update(idx,td)

def add_transition(transition):

	global replay_buffer, replay_buffer_size
	
	#replay_buffer.append(transition)
	replay_buffer.add(transition)

	#if len(replay_buffer)>replay_buffer_size:
	#	del replay_buffer[:1]


def save():

	last_episodes = np.array(episode_timestep_history[-200:])
	print('saving')
	print('STATUS:')
	print('Episilon: ', e)
	print('EPISODES COMPLETED: ', i_episode+1)
	print('timestep: ', timestep)
	print('Mean number of timesteps: ', last_episodes.mean())
	print('GOAL REACHED PERCENTAGE: ', np.array([x!=env.max_timesteps for x in last_episodes]).mean())
	print('Running distance: ', running_reward)
	print('PER BETA : ', replay_buffer.beta)
	print('temporal diff running average', temporal_diff_mean)
	print('TIME ELAPSED: ', timedelta(seconds = time()-t0))
	print('Q VALUES for the initial state:', Q_net.predict(normalize(np.array([s_start])))[0])
	print('------------------------------------')
	plot_reward_history()
	plot_episode_lenght_history()
	Q_target_net.set_weights(Q_net.get_weights()) 
	Q_net.save("DQN.h5")
	pickle.dump(scaler, open('scaler.pkl', 'wb'))

t0 = time()
get_reward = get_reward1

for i_episode in range(episodes):
	s = env.reset()
	Goal = s[-2:].copy()
	s_start = s
	cumulative_reward = 0
	final_state = None
	buffer_accumulator = list()

	for t in range(max_timesteps):
		#env.render()
		# Epsilon greedy
		e = max(initial_episilon - exploration_linear_decay* (timestep-random_steps) , episilon)
		a = get_episilon_greedy_action(s, e) 
		
		ss, r, done, info = env.step(a)	
		r = get_reward(s,a,ss,Goal)
		#print(r)
		#print(s)
		
		cumulative_reward = cumulative_reward + r	
		final_state = ss[0:2].copy()

		# Storing experience
		experience = (s,a,r,ss, done)
		#print(experience)
		add_transition(experience)
		buffer_accumulator.append(experience)
		s = ss
		
		if timestep > 100000 and timestep%update_frequency==0:
			#print('training')
			train()

		if timestep%C ==0:
			save()


		timestep += 1

		if done:

			#print("Episode", i_episode," done in ", t, " timesteps")
			if Hindsight_experience_replay:

				#print('alsd')
				#print(buffer_accumulator)
				extra_goals = [(x[0][0],x[0][1]) for x in random.sample(buffer_accumulator,min(4, len(buffer_accumulator)))]
				
				for eg in extra_goals:
				
					final_x, final_y = eg
					for ex in buffer_accumulator:

						s,a,r,ss, done = ex
						
						s = s.copy()
						ss = ss.copy()
						s[-2] = final_x
						s[-1] = final_y
						ss[-2] = final_x
						ss[-1] = final_y


						r = get_reward(s,a,ss,eg)
						done = r==0
						new_experience = (s,a,r,ss, done)
						#print(new_experience)
						add_transition(new_experience)


			"""
			if i_episode%16 ==0 and timestep >= 10000:

				print('Update count', (update_count%C)/C, end = '\r')
				for train_step in range(40):
					train()
					update_count +=1
			
				if update_count%C ==0:
					save()
			"""

			episode_timestep_history.append(t)
			dist = np.sqrt((final_state[0] - Goal[0])**2 + (final_state[1] - Goal[1])**2)
			reward_history.append(dist)
			running_reward = running_reward* (1-average_proportion) + average_proportion * dist
			break
env.close()
