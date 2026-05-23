"""Planet implementation for the new object model."""

import itertools
import math

import pygame

import constants
from .base import Body


class Planet(Body):
	cycle_colors = itertools.cycle([
		constants.COLOR_MERCURY,
		constants.COLOR_VENUS,
		constants.COLOR_EARTH,
		constants.COLOR_MARS,
		constants.COLOR_JUPITER,
		constants.COLOR_SATURN,
		constants.COLOR_URANUS,
		constants.COLOR_NEPTUNE,
	])

	def __init__(self, x, y, radius, mass, name, is_inner_planet=False, color=None):
		super().__init__(x, y, radius, mass, name=name, color=color or next(Planet.cycle_colors))
		self.is_inner_planet = is_inner_planet

		self.orbit_start_index = 0
		self.last_complete_orbit = []
		self.orbit_count = 0
		self.prev_x = x
		self.prev_y = y
		self.orbit_detected = False
		self.has_crossed_reference = False

		self.flash_timer = 0
		self.flash_duration = 10

	def update_position(self, current_solarsystem):
		self.prev_x = self.x
		self.prev_y = self.y

		super().update_position(current_solarsystem)
		self._check_orbit_completion()

		if self.flash_timer > 0:
			self.flash_timer -= 1

	def _check_orbit_completion(self):
		if len(self.orbit) < 100:
			return

		if self.orbit_start_index < len(self.orbit):
			start_point = self.orbit[self.orbit_start_index]
			current_point = (self.x, self.y)
			distance_to_start = math.sqrt(
				(current_point[0] - start_point[0])**2 +
				(current_point[1] - start_point[1])**2
			)
			threshold = 0.01 * self.AU

			if distance_to_start < threshold and not self.orbit_detected:
				if len(self.orbit) - self.orbit_start_index > 50:
					self.orbit_count += 1
					self.orbit_detected = True
					self.orbit = [(self.x, self.y)]
					self.orbit_start_index = 0
					self.flash_timer = self.flash_duration

			elif distance_to_start > threshold * 2:
				self.orbit_detected = False

	def draw(self, display_surface, distance_scale, screen_offset_x=0, screen_offset_y=0):
		x, y = self._screen_position(distance_scale, screen_offset_x, screen_offset_y)

		if self.draw_line and len(self.orbit) >= 2:
			orbit_fade_multiplier = max(0.1, 1.0 - (self.orbit_count * 0.1))
			fade_scale = 1.0
			orbit_points = self._orbit_points(distance_scale, screen_offset_x, screen_offset_y)

			for i in range(1, len(orbit_points)):
				distance = len(orbit_points) - i
				distance_fade_factor = max(0, min(255, int(255 * (distance / len(orbit_points)) * fade_scale)))
				combined_fade = orbit_fade_multiplier * (1 - distance_fade_factor / 255)

				faded_color = (
					int(self.color[0] * combined_fade + constants.COLOR_BACKGROUND[0] * (1 - combined_fade)),
					int(self.color[1] * combined_fade + constants.COLOR_BACKGROUND[1] * (1 - combined_fade)),
					int(self.color[2] * combined_fade + constants.COLOR_BACKGROUND[2] * (1 - combined_fade)),
				)

				pygame.draw.line(display_surface, faded_color, orbit_points[i - 1], orbit_points[i], 1)

		pygame.draw.circle(display_surface, self.color, (int(x), int(y)), max(1, int(self.radius)))

		if self.flash_timer > 0:
			flash_intensity = self.flash_timer / self.flash_duration
			flash_radius = int(self.radius * (1.5 + flash_intensity))
			flash_color = (255, 255, 200)
			pygame.draw.circle(display_surface, flash_color, (int(x), int(y)), flash_radius, 2)
