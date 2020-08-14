# File for storing utils
from enum import Enum

class Axis(Enum):

	LATERAL = (0,1)
	VERTICAL = (1,0)

def get_velocity(car, axis: Axis):
	"""
	Returns the projection of the car's velocity w.r.t some of his axis: either LATERAL or VERTICAL 
	"""

	normal = car.GetWorldVector(axis.value)
	velocity = car.linearVelocity
	projection = (np.dot(velocity, normal)/ (np.linalg.norm(normal)**2) )*normal
		
	return projection