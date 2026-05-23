"""Asteroid implementation for the new object model."""

import pygame

import constants
from .base import Body


class Asteroid(Body):
	def __init__(self, x, y, radius, mass, color=(192, 192, 192), name="Asteroid"):
		super().__init__(x, y, radius, mass, name=name, color=color)
		self.draw_line = False

	def update_position(self, current_solarsystem):
		sun = current_solarsystem[0]
		fx, fy = self.attraction(sun)
		self.x_vel += fx / self.mass * self.TIMESTEP
		self.y_vel += fy / self.mass * self.TIMESTEP
		self.x += self.x_vel * self.TIMESTEP
		self.y += self.y_vel * self.TIMESTEP

	def draw(self, display_surface, distance_scale, screen_offset_x=0, screen_offset_y=0):
		x, y = self._screen_position(distance_scale, screen_offset_x, screen_offset_y)

		if 0 <= x <= constants.WIDTH and 0 <= y <= constants.HEIGHT:
			pygame.draw.circle(display_surface, self.color, (int(x), int(y)), max(1, int(self.radius)))
