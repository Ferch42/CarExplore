# Class Terrain for applying forces in the car

from abc import ABC, abstractmethod
from pygame.locals import (QUIT, KEYDOWN, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT)
from enums.Axis import Axis
import numpy as np
from events.CarEvent import CarEvent

class Terrain(ABC):

	_ACCELERATION = 1000
	_TORQUE = 200
	COLOR = (255,255,255,255) # White
	
	@abstractmethod
	def apply_ordinary_forces(car):
		pass

	def handle_impulse_event(car, event: CarEvent):
		
		# Acceleration
		if event == CarEvent.ACCELERATE:
			car.ApplyForce(force= Terrain._ACCELERATION*car.GetWorldVector(Axis.VERTICAL.value), point=car.worldCenter , wake=True)

		# Brake
		if event == CarEvent.BRAKE:
			car.ApplyForce(force= -Terrain._ACCELERATION*car.GetWorldVector(Axis.VERTICAL.value), point=car.worldCenter, wake=True)
		
		# Turn left
		if event == CarEvent.TURN_LEFT:
			car.ApplyTorque(Terrain._TORQUE, wake = True)

		# Turn right
		if event == CarEvent.TURN_RIGHT:
			car.ApplyTorque(-Terrain._TORQUE, wake = True)

	def get_impulse(car, axis: Axis):

		return car.mass * - Terrain.get_velocity(car, axis)

	def get_velocity(car, axis: Axis):
		"""
		Returns the projection of the car's velocity w.r.t some of his axis: either LATERAL or VERTICAL 
		"""

		normal = car.GetWorldVector(axis.value)
		velocity = car.linearVelocity
		projection = (np.dot(velocity, normal)/ (np.linalg.norm(normal)**2) )*normal
			
		return projection