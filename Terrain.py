# Class Terrain for applying forces in the car

from abc import ABC, abstractmethod
from pygame.event import Event
from pygame.locals import (QUIT, KEYDOWN, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT)
from Axis import Axis
import numpy as np

class Terrain(ABC):

	_ACCELERATION = 1000
	_TORQUE = 200
	COLOR = (255,255,255,255) # White
	
	@abstractmethod
	def apply_ordinary_forces(car):
		pass

	def handle_impulse_event(car, event: Event):
		
		# Acceleration
		if event.type == KEYDOWN and event.key == K_UP:
			car.ApplyForce(force= Terrain._ACCELERATION*car.GetWorldVector(Axis.VERTICAL.value), point=car.worldCenter , wake=True)

		# Brake
		if event.type == KEYDOWN and event.key == K_DOWN:

			car.ApplyForce(force= -Terrain._ACCELERATION*car.GetWorldVector(Axis.VERTICAL.value), point=car.worldCenter, wake=True)
		
		# Turn left
		if event.type == KEYDOWN and event.key == K_LEFT:

			car.ApplyTorque(Terrain._TORQUE, wake = True)

		# Turn right
		if event.type == KEYDOWN and event.key == K_RIGHT:

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