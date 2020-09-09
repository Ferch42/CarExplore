# CarExplore application

from ApplicationFactory import ApplicationFactory
from pygame.locals import (QUIT, KEYDOWN, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT)
import pygame

app_name = "GOAL_APP"

game_controller, interface = ApplicationFactory.create(app_name)


# --- main game loop ---
running = True

while running:

	# Updates physics engine
	game_controller.update()

	for event in pygame.event.get():

		if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
			# The user closed the window or pressed escape
			running = False

		game_controller.handle_event(event)
			
			
	interface.render()
	game_controller.step()

interface.quit()
print('Done!')