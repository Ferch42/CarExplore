from pygame.locals import (QUIT, KEYDOWN, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT)
from pygame.event import EventType
from events.CarEvent import CarEvent

class EventFactory:

	def create(event):

		if type(event) == EventType:

			if event.type == KEYDOWN:
				
				# Acceleration	
				if event.key == K_UP:
					return CarEvent.ACCELERATE 

				# Brake
				if event.key == K_DOWN:
					return CarEvent.BRAKE 
					
				# Turn left
				if event.key == K_LEFT:
					return CarEvent.TURN_LEFT 

				# Turn right
				if event.key == K_RIGHT:
					return CarEvent.TURN_RIGHT 
			else:
				return CarEvent.NULL

		if type(event) == int:

			if event == 0:
				return CarEvent.NULL

			if event == 1:
				return CarEvent.ACCELERATE

			if event == 2:
				return CarEvent.BRAKE

			if event == 3:
				return CarEvent.TURN_LEFT

			if event == 4:
				return CarEvent.TURN_RIGHT




