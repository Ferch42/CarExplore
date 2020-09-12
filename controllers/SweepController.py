from controllers.GameController import GameController
import numpy as np

class SweepController(GameController):

	def __init__(self):

		super().__init__()
		self.grid_size = 10
		self.grid = np.full((int(self.WORLD_WIDTH/self.grid_size), int(self.WORLD_HEIGHT/self.grid_size)), False, dtype = bool)
		self.grid_render_size = self.grid_size*self.PPM
		self.block_render_size = self.grid_size *self.PPM
		self.occupancy_square_percentage = 0.1

	def get_car_grid_position(self):

		car_x, car_y = self.car.worldCenter
		return (int(car_x/self.grid_size), int(car_y/self.grid_size))

	def update(self):

		super().update()
		x, y = self.get_car_grid_position()
		self.grid[x][y] = True


	def get_occupancy_grid(self):

		return np.flip(self.grid, 1)

	def get_grid_lines(self):
		"""
		Returns to the interface the postions of the grid lines to render
		"""

		# Calculates the horizontal lines positions
		horizontal_lines = []
		x_aux = self.grid_render_size

		while x_aux<self.SCREEN_WIDTH:

			horizontal_lines.append(((x_aux, 0),(x_aux, self.SCREEN_HEIGHT)))
			x_aux += self.grid_render_size

		# Calculates the vertical lines positions
		vertival_lines = []
		y_aux = self.grid_render_size
		
		while y_aux < self.SCREEN_HEIGHT:

			vertival_lines.append(((0, y_aux), (self.SCREEN_WIDTH, y_aux)))
			y_aux += self.grid_render_size

		return vertival_lines+horizontal_lines 

	def get_occupancy_squares(self):
		"""
		Returns the occupancy squares of the grid
		"""

		squares = []
		occupation_grid = self.get_occupancy_grid()
		n_rows , n_columns = occupation_grid.shape

		for x in range(n_rows):
			for y in range(n_columns):
				x_coord = x*self.block_render_size
				y_coord = y*self.block_render_size
				square_lenght = self.block_render_size* self.occupancy_square_percentage

				squares.append({"RECT": (x_coord, y_coord,square_lenght, square_lenght), "OCCUPANCY": occupation_grid[x][y]})

		return squares
