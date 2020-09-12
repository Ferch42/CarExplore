#Application Factory

from controllers.GameController import GameController
from controllers.GoalController import GoalController
from controllers.SweepController import SweepController
from views.Interface import Interface
from views.GoalInterface import GoalInterface
from views.SweepInterface import SweepInterface

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
		
		elif app == 'SWEEP_APP':

			controller = SweepController()
			interface = SweepInterface()
		else:
			raise NameException("Not a valid App")

		interface.set_controller(controller)

		return (controller, interface)
