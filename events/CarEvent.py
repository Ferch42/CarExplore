#Car Event Enum

from enum import Enum

class CarEvent(Enum):

	ACCELERATE = 0
	BRAKE = 1
	TURN_RIGHT = 2
	TURN_LEFT = 3
	NULL = 4