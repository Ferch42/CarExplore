import numpy as np
import gym
import tensorflow as tf
from tensorflow.keras import layers
import numpy as np
import matplotlib.pyplot as plt
import random
from GridEnvironment import GridEnvironment
from sklearn.preprocessing import StandardScaler
from Planner import Planner
import pickle
import time
from tqdm import tqdm

env = GridEnvironment()
num_states = env.observation_space.shape[0] +2
num_actions = env.action_space.shape[0]

def get_actor():
	# Initialize weights between -3e-3 and 3-e3
	last_init = tf.random_uniform_initializer(minval=-0.003, maxval=0.003)

	inputs = layers.Input(shape=(num_states,))
	out = layers.Dense(400, activation="relu")(inputs)
	out = layers.Dense(300, activation="relu")(out)
	#out = layers.Dense(64, activation="relu")(out)
	outputs = layers.Dense(env.action_space.shape[0], activation="tanh", kernel_initializer=last_init)(out)

	# Our upper bound is 2.0 for Pendulum.
	outputs = outputs * tf.convert_to_tensor(env.action_space.high)
	model = tf.keras.Model(inputs, outputs)
	return model


def get_critic():
	# State as input
	state_input = layers.Input(shape=(num_states))
	state_out = layers.Dense(32, activation="relu")(state_input)
	#state_out = layers.Dense(32, activation="relu")(state_out)

	# Action as input
	action_input = layers.Input(shape=(num_actions))
	action_out = layers.Dense(32, activation="relu")(action_input)

	# Both are passed through seperate layer before concatenating
	concat = layers.Concatenate()([state_out, action_out])

	out = layers.Dense(400, activation="relu")(concat)
	out = layers.Dense(300, activation="relu")(out)
	outputs = layers.Dense(1)(out)

	# Outputs single value for give state-action
	model = tf.keras.Model([state_input, action_input], outputs)

	return model


actor_model = get_actor()
critic_model = get_critic()

target_actor = get_actor()
target_critic = get_critic()

print("ACTOR SUMMARY")
print(actor_model.summary())

print("CRITIC SUMMARY")
print(critic_model.summary())


actor_model.load_weights('actor.h5')
critic_model.load_weights('critic.h5')

target_actor.load_weights('target_actor.h5')
target_critic.load_weights('target_critic.h5')

scaler = pickle.load(open('scaler.pkl', 'rb'))

timesteps_hist = pickle.load(open('Planner_hist.pkl', 'rb'))
sweep_percentage = []

for i in range(200):
	
	s = env.reset()
	p = Planner(env.controller.WORLD_WIDTH, env.controller.WORLD_HEIGHT, env.controller.grid_size, actor_model, critic_model,scaler)
	print(i)
	timestep = 0

	while(True):

		#env.render()
		#a = np.random.uniform(-100,100,2)
		#a = ou_noise()
		#print(a)
		#print("State: ",s)
		a = p.get_action(s)
		a = np.array(a)
		a = a + np.random.normal(0,10,2)
		ss, r, done, info = env.step(a)	
		timestep +=1

		s = ss
		if done:
			print("Done in :", timestep)
			sp  = p.get_goal_sweep_percentage()
			print("Sweep percentage: ", sp)
			sweep_percentage.append(sp)
			timesteps_hist.append(timestep)
			break

pickle.dump(timesteps_hist, open('Planner_hist.pkl', 'wb'))
pickle.dump(sweep_percentage, open('sweep_percentage.pkl', 'wb'))