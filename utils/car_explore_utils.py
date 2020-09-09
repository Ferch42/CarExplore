# File for storing utils
from controllers.Area import Area
from enums.Axis import Axis
import os

# Functions 

def deserialize_areas():
	"""
	Deserializes and builds AREA objects 
	"""
	areas_list = []

	areas = os.listdir('./areas/')
		
	for a in areas:
		area_json = open('./areas/'+ a).read()
		area_dict = eval(area_json)
		new_area = Area(area_dict['lower_bound'], area_dict['upper_bound'], area_dict['terrain'])
		areas_list.append(new_area)


	return areas_list

def deserialize_obstacles():
	"""
	Deserializes and obstacles
	"""
	obstacles_list = []

	obstacles = os.listdir('./obstacles/')
		
	for o in obstacles:
		obstacle_json = open('./obstacles/'+ o).read()
		obstacle_dict = eval(obstacle_json)
		obstacles_list.append(obstacle_dict['vertices'])

	return obstacles_list
