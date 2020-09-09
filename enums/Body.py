# Body enum
from enum import Enum
from Box2D.b2 import staticBody, dynamicBody

class Body(Enum):

	DYNAMIC = dynamicBody
	STATIC = staticBody
