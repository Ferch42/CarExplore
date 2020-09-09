#Application Factory

from controllers.GameController import GameController
from controllers.GoalController import GoalController
from views.Interface import Interface
from views.GoalInterface import GoalInterface

class ApplicationFactory:

	def create(app):

		controller = None
		interface = None

		if app == 'DEFAULT_APP':

			controller = GameController()
			interface = Interface()
			
		elif app == 'GOAL_APP':

			controller = GoalController()
			interface = GoalInterface()
		
		else:
			raise NameException("Not a valid App")

		interface.set_controller(controller)

		return (controller, interface)
