# Asphalt Terrain

from Terrain import Terrain
from Axis import Axis

class AsphaltTerrain(Terrain):

	COLOR = (127,127,127,0) # Gray

	def apply_ordinary_forces(car):

		lat_imp = AsphaltTerrain.get_impulse(car, Axis.LATERAL) 
		car.ApplyLinearImpulse(impulse = lat_imp, point= car.worldCenter, wake = True)
		car.ApplyAngularImpulse(impulse = 0.001*car.inertia * - car.angularVelocity, wake = True)

		fwd_imp = AsphaltTerrain.get_impulse(car, Axis.VERTICAL) * 0.01 
		car.ApplyLinearImpulse(impulse = fwd_imp, point=car.worldCenter, wake = True)