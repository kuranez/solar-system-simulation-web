"""Earth preset factory."""

import constants
from simulation.solarsystem_scale import calculate_scaled_sizes

from ..planet import Planet


def create_earth(distance_scale=constants.DEFAULT_SCALE):
	scaled_sizes = calculate_scaled_sizes(distance_scale)
	earth_data = next((planet for planet in constants.PLANETS_DATA if planet["name"] == "Earth"), None)

	if earth_data is None:
		return None

	earth_radius = scaled_sizes.get("Earth", earth_data["radius"])
	earth = Planet(
		earth_data["position"] * constants.AU,
		0,
		earth_radius,
		earth_data["mass"],
		earth_data["name"],
		earth_data["is_inner"],
		color=constants.COLOR_EARTH,
	)
	earth.y_vel = earth_data["velocity"]
	return earth
