from pygame.locals import (QUIT, KEYDOWN, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT)
from pygame.event import EventType
from events.CarEvent import CarEvent

class EventFactory:

	def create(event):

		if type(event) == EventType:

			# Acceleration	
			if event.type == KEYDOWN and event.key == K_UP:
				return CarEvent.ACCELERATE 

			# Brake
			if event.type == KEYDOWN and event.key == K_DOWN:
				return CarEvent.BRAKE 
				
			# Turn left
			if event.type == KEYDOWN and event.key == K_LEFT:
				return CarEvent.TURN_LEFT 

			# Turn right
			if event.type == KEYDOWN and event.key == K_RIGHT:
				return CarEvent.TURN_RIGHT 



