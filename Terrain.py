# Class Terrain for applying forces in the car

from abc impor ABC, abstractmethod
from pygame.event import Event
from pygame.locals import (QUIT, KEYDOWN, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT)
from utils import *

class Terrain(ABC):

	_ACCELERATION = 1000
	_TORQUE = 200
	
	@abstractmethod
	def apply_ordinary_forces(car):
		pass

	def handle_impulse_event(car, event: Event):
		
		# Acceleration
		if event.type == KEYDOWN and event.key == K_UP:
			car.ApplyForce(force= Terrain._ACCELERATION*car.GetWorldVector(Axis.VERTIVAL.value), point=car.worldCenter , wake=True)

		# Brake
		if event.type == KEYDOWN and event.key == K_DOWN:

			car.ApplyForce(force= -Terrain._ACCELERATION*car.GetWorldVector(Axis.VERTIVAL.value), point=car.worldCenter, wake=True)
		
		# Turn left
		if event.type == KEYDOWN and event.key == K_LEFT:

			car.ApplyTorque(Terrain._TORQUE, wake = True)

		# Turn right
		if event.type == KEYDOWN and event.key == K_RIGHT:

			car.ApplyTorque(-Terrain._TORQUE, wake = True)

	def get_impulse(car, axis: Axis):

		return car.mass * get_velocity(car, axis)

