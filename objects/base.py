"""Shared base body implementation for the new object model."""

from __future__ import annotations

import math

import pygame

import constants


class Body:
	AU = constants.AU
	G = constants.G
	TIMESTEP = constants.TIMESTEP

	def __init__(self, x, y, radius, mass, name="Body", color=(0, 0, 0), is_sun=False):
		self.x = x
		self.y = y
		self.radius = radius
		self.original_radius = radius
		self.mass = mass
		self.name = name
		self.color = color

		self.is_sun = is_sun
		self.sun = is_sun
		self.distance_to_sun = 0
		self.static_body: bool = False
		self.child_of: Body | None = None
		self.parent_body: Body | None = None

		self.orbit = []
		# Track orbit completions when available (planets set/use this)
		self.orbit_count = 0
		self.x_vel = 0.0
		self.y_vel = 0.0
		self.draw_line = True
		# Children bodies (moons, rings, etc.) — factories should append here
		self.children = []

	def update_distance_to_sun(self, sun):
		if not self.is_sun:
			distance_x = sun.x - self.x
			distance_y = sun.y - self.y
			self.distance_to_sun = math.sqrt(distance_x**2 + distance_y**2)

	def attraction(self, other):
		dx, dy = other.x, other.y
		distance_x = dx - self.x
		distance_y = dy - self.y
		distance = math.sqrt(distance_x**2 + distance_y**2)

		if distance == 0:
			return 0.0, 0.0

		force = self.G * self.mass * other.mass / distance**2
		theta = math.atan2(distance_y, distance_x)
		fx = math.cos(theta) * force
		fy = math.sin(theta) * force

		return fx, fy

	def update_position(self, current_solarsystem):
		if getattr(self, "static_body", False):
			return

		total_fx = 0
		total_fy = 0

		sun = None
		for body in current_solarsystem:
			if getattr(body, "is_sun", False) or getattr(body, "sun", False):
				sun = body
				break

		if sun is not None:
			self.update_distance_to_sun(sun)

		for body in current_solarsystem:
			if self == body:
				continue

			fx, fy = self.attraction(body)
			total_fx += fx
			total_fy += fy

		self.x_vel += total_fx / self.mass * self.TIMESTEP
		self.y_vel += total_fy / self.mass * self.TIMESTEP

		self.x += self.x_vel * self.TIMESTEP
		self.y += self.y_vel * self.TIMESTEP

		self.orbit.append((self.x, self.y))
		if len(self.orbit) > 20000:
			self.orbit.pop(0)

	def _screen_position(self, distance_scale, screen_offset_x=0, screen_offset_y=0):
		x = self.x * distance_scale + screen_offset_x
		y = self.y * distance_scale + screen_offset_y
		return x, y

	def _orbit_points(self, distance_scale, screen_offset_x=0, screen_offset_y=0):
		return [
			(
				px * distance_scale + screen_offset_x,
				py * distance_scale + screen_offset_y,
			)
			for px, py in self.orbit
		]

	def _draw_orbit_trail(self, display_surface, distance_scale, screen_offset_x=0, screen_offset_y=0, fade_scale=1.5):
		if not self.draw_line or len(self.orbit) < 2:
			return

		orbit_points = self._orbit_points(distance_scale, screen_offset_x, screen_offset_y)
		for i in range(1, len(orbit_points)):
			distance = len(orbit_points) - i
			fade_factor = max(0, min(255, int(255 * (distance / len(orbit_points)) * fade_scale)))
			faded_color = (
				int(self.color[0] * (1 - fade_factor / 255) + constants.COLOR_BACKGROUND[0] * (fade_factor / 255)),
				int(self.color[1] * (1 - fade_factor / 255) + constants.COLOR_BACKGROUND[1] * (fade_factor / 255)),
				int(self.color[2] * (1 - fade_factor / 255) + constants.COLOR_BACKGROUND[2] * (fade_factor / 255)),
			)
			pygame.draw.line(display_surface, faded_color, orbit_points[i - 1], orbit_points[i], 1)

	def draw(self, display_surface, distance_scale, screen_offset_x=0, screen_offset_y=0):
		x, y = self._screen_position(distance_scale, screen_offset_x, screen_offset_y)
		self._draw_orbit_trail(display_surface, distance_scale, screen_offset_x, screen_offset_y)
		pygame.draw.circle(display_surface, self.color, (int(x), int(y)), max(1, int(self.radius)))
