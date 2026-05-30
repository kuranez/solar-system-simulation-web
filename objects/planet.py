"""Planet implementation for the new object model."""

import itertools

import pygame

import constants
from .base import Body


class Planet(Body):
	# Cycle through planet colors for each new instance if not specified
	# Kept here in the class to maintain state across instances without global variables
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

		self.flash_timer = 0
		self.flash_duration = 10

	def update_position(self, current_solarsystem):
		super().update_position(current_solarsystem)

		if self.flash_timer > 0:
			self.flash_timer -= 1

	def draw(self, display_surface, distance_scale, screen_offset_x=0, screen_offset_y=0):
		super().draw(display_surface, distance_scale, screen_offset_x, screen_offset_y)
		x, y = self._screen_position(distance_scale, screen_offset_x, screen_offset_y)
