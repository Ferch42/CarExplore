import numpy as np
from matplotlib import pyplot as plt
import pickle

ep_reward = pickle.load(open('ep_reward_list.pkl', 'rb')) 
dist_list = pickle.load(open('dis_list.pkl', 'rb'))

def smooth(l):

	nl = []
	for i in range(1, len(l)):
		nl.append(np.mean(l[max(0, i-100):i]))

	return nl

def plot(l, title, y_axis_name):

	plt.ylabel(y_axis_name)
	plt.xlabel("Número de episódios")
	plt.title(title)
	plt.plot(l)
	plt.show()
