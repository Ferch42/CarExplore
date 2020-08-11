from config import *
import pygame
from pygame.locals import (QUIT, KEYDOWN, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT)
import Box2D  
from Box2D.b2 import (world, polygonShape, staticBody, dynamicBody)
import numpy as np

# --- pygame setup ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('CarExplore')
clock = pygame.time.Clock()

# --- pybox2d world setup ---
# Create the world
world = world(gravity=(0, 0), doSleep=True)

# And a static body to hold the ground shape
# bottom floor

ground_body = world.CreateStaticBody(
	position=(0, -1),
	shapes=polygonShape(box=(100, 1)),
)


# Create a dynamic body
dynamic_body = world.CreateDynamicBody(position=(10, 15))
dynamic_body.angularDamping = 0.1
# And add a box fixture onto it (with a nonzero density, so it will move)
box = dynamic_body.CreatePolygonFixture(box=(2, 1), density=1, friction=0.3)

colors = {
	staticBody: (127, 127, 127, 255),
	dynamicBody: (255,165,0, 255),
}

def get_lateral_velocity():
	lateral_normal = dynamic_body.GetWorldVector((0,1))
	velocity = dynamic_body.linearVelocity
	projection = (np.dot(velocity, lateral_normal)/ (np.linalg.norm(lateral_normal)**2) )*lateral_normal
	return projection

def get_foward_velocity():
	lateral_normal = dynamic_body.GetWorldVector((1,0))
	velocity = dynamic_body.linearVelocity
	projection = (np.dot(velocity, lateral_normal)/ (np.linalg.norm(lateral_normal)**2) )*lateral_normal
	return projection
# --- main game loop ---
running = True

linear_acceleration = 10
angular_acceletarion = Box2D.b2_pi/2
while running:

	# Apply lateral impulse to counter lateral and angular velocities
	imp = dynamic_body.mass * - get_lateral_velocity()
	dynamic_body.ApplyLinearImpulse(impulse = imp, point=dynamic_body.worldCenter, wake = True)
	dynamic_body.ApplyAngularImpulse(impulse = 0.001*dynamic_body.inertia * - dynamic_body.angularVelocity, wake = True)

	# Apply drag
	imp = dynamic_body.mass * - get_foward_velocity() * 0.01
	dynamic_body.ApplyLinearImpulse(impulse = imp, point=dynamic_body.worldCenter, wake = True)

	# Check the event queue
	for event in pygame.event.get():
		if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
			# The user closed the window or pressed escape
			running = False

		if event.type == KEYDOWN and event.key == K_UP:
			dynamic_body.ApplyForce(force= 1000*dynamic_body.GetWorldVector((1,0)), point=dynamic_body.worldCenter , wake=True)


		if event.type == KEYDOWN and event.key == K_DOWN:

			dynamic_body.ApplyForce(force=-1500*dynamic_body.GetWorldVector((1,0)), point=dynamic_body.worldCenter, wake=True)
			
		if event.type == KEYDOWN and event.key == K_LEFT:

			dynamic_body.ApplyTorque(200, wake = True)

		if event.type == KEYDOWN and event.key == K_RIGHT:

			dynamic_body.ApplyTorque(-200, wake = True)
			
			

	screen.fill((127, 127, 127, 0))
	# Draw the world
	for body in (ground_body, dynamic_body):  # or: world.bodies
		# The body gives us the position and angle of its shapes
		for fixture in body.fixtures:
			# The fixture holds information like density and friction,
			# and also the shape.
			shape = fixture.shape

			# Naively assume that this is a polygon shape. (not good normally!)
			# We take the body's transform and multiply it with each
			# vertex, and then convert from meters to pixels with the scale
			# factor.
			vertices = [(body.transform * v) * PPM for v in shape.vertices]

			# But wait! It's upside-down! Pygame and Box2D orient their
			# axes in different ways. Box2D is just like how you learned
			# in high school, with positive x and y directions going
			# right and up. Pygame, on the other hand, increases in the
			# right and downward directions. This means we must flip
			# the y components.
			vertices = [(v[0], SCREEN_HEIGHT - v[1]) for v in vertices]
			#print(vertices)
			pygame.draw.polygon(screen, colors[body.type], vertices)

	# Make Box2D simulate the physics of our world for one step.
	# Instruct the world to perform a single step of simulation. It is
	# generally best to keep the time step and iterations fixed.
	# See the manual (Section "Simulating the World") for further discussion
	# on these parameters and their implications.
	world.Step(TIME_STEP, 10, 10)

	# Flip the screen and try to keep at the target FPS
	pygame.display.flip()
	clock.tick(TARGET_FPS)

pygame.quit()
print('Done!')