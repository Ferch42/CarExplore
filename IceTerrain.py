# Ice Terrain

from Terrain import Terrain
from utils import *

class IceTerrain(Terrain):

	def apply_ordinary_forces(car):

		lat_imp = AsphaltTerrain.get_impulse(car, Axis.LATERAL) * 0.1
		car.ApplyLinearImpulse(impulse = lat_imp, point= car.worldCenter, wake = True)
		car.ApplyAngularImpulse(impulse = 0.001*car.inertia * - car.angularVelocity, wake = True)

		fwd_imp = AsphaltTerrain.get_impulse(car, Axis.VERTICAL) * 0.00001
		car.ApplyLinearImpulse(impulse = fwd_imp, point=car.worldCenter, wake = True)