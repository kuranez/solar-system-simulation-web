"""Shared physics helpers for the solar system simulation."""

from __future__ import annotations

import math

import constants


def circular_orbital_speed(central_mass, radius):
	"""Return circular orbital speed (m/s) around a central mass at a radius."""
	return math.sqrt(constants.G * central_mass / radius)


def update_distance_to_sun(body, sun):
	"""Update a body's cached distance to the Sun-like reference body."""
	if getattr(body, "is_sun", False):
		return

	distance_x = sun.x - body.x
	distance_y = sun.y - body.y
	body.distance_to_sun = math.sqrt(distance_x**2 + distance_y**2)


def attraction(body, other):
	"""Calculate gravitational force components exerted on body by other."""
	distance_x = other.x - body.x
	distance_y = other.y - body.y
	distance = math.sqrt(distance_x**2 + distance_y**2)

	if distance == 0:
		return 0.0, 0.0

	force = constants.G * body.mass * other.mass / distance**2
	theta = math.atan2(distance_y, distance_x)
	fx = math.cos(theta) * force
	fy = math.sin(theta) * force

	return fx, fy


def find_sun(current_solarsystem):
	"""Return the first body flagged as the Sun, if present."""
	for body in current_solarsystem:
		if getattr(body, "is_sun", False) or getattr(body, "sun", False):
			return body

	return None


def advance_body(body, current_solarsystem, timestep=None):
	"""Advance a body using Newtonian gravity against the supplied system."""
	if getattr(body, "static_body", False):
		return

	total_fx = 0.0
	total_fy = 0.0
	timestep = timestep if timestep is not None else getattr(body, "TIMESTEP", constants.TIMESTEP)

	sun = find_sun(current_solarsystem)
	if sun is not None:
		update_distance_to_sun(body, sun)

	for other in current_solarsystem:
		if body == other:
			continue

		fx, fy = attraction(body, other)
		total_fx += fx
		total_fy += fy

	body.x_vel += total_fx / body.mass * timestep
	body.y_vel += total_fy / body.mass * timestep

	body.x += body.x_vel * timestep
	body.y += body.y_vel * timestep

	# Store orbit points relative to a reference frame so orbit completion
	# detection is robust when the parent (e.g., Earth) is also moving.
	if getattr(body, "parent_body", None) is not None:
		ref = body.parent_body
		rel_x = body.x - ref.x
		rel_y = body.y - ref.y
	elif sun is not None:
		ref = sun
		rel_x = body.x - ref.x
		rel_y = body.y - ref.y
	else:
		rel_x = body.x
		rel_y = body.y

	body.orbit.append((rel_x, rel_y))
	if len(body.orbit) > 50000:
		body.orbit.pop(0)

	orbit_checker = getattr(body, "_check_orbit_completion", None)
	if callable(orbit_checker):
		# Provide the full system so the checker can compute relative positions
		orbit_checker(current_solarsystem)