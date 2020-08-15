# File for storing utils
from enum import Enum
from Box2D.b2 import staticBody, dynamicBody
# Enum Classes
class Axis(Enum):

	LATERAL = (0,1)
	VERTICAL = (1,0)

class Body(Enum):

	DYNAMIC = dynamicBody
	STATIC = staticBody

# Functions 
def get_velocity(car, axis: Axis):
	"""
	Returns the projection of the car's velocity w.r.t some of his axis: either LATERAL or VERTICAL 
	"""

	normal = car.GetWorldVector(axis.value)
	velocity = car.linearVelocity
	projection = (np.dot(velocity, normal)/ (np.linalg.norm(normal)**2) )*normal
		
	return projection

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
