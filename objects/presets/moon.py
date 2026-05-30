"""Moon preset factory."""

import constants

from ..moon import Moon


def create_moon(parent_body, distance_scale=constants.DEFAULT_SCALE):
	moon_data = constants.MOON_DATA
	moon_radius = moon_data["radius"]
	# Use the physical average distance (meters). Do not scale by UI distance_scale.
	distance = moon_data["average_distance"]

	moon = Moon(
		parent_body.x - distance,
		parent_body.y,
		moon_radius,
		moon_data["mass"],
		name=moon_data["name"],
		color=moon_data["color"],
		parent_body=parent_body,
		x_vel=parent_body.x_vel,
		y_vel=parent_body.y_vel + moon_data["orbital_velocity"],
	)
	return moon