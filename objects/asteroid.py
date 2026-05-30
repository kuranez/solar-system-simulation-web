"""Asteroid implementation for the new object model."""

import pygame

import constants
from .base import Body


class Asteroid(Body):
	def __init__(self, x, y, radius, mass, color=(192, 192, 192), name="Asteroid"):
		super().__init__(x, y, radius, mass, name=name, color=color)
		self.draw_line = False

	def update_position(self, current_solarsystem, timestep=None, frame_timestep=None):
		sun = current_solarsystem[0]
		fx, fy = self.attraction(sun)
		step_dt = timestep if timestep is not None else self.TIMESTEP
		self.x_vel += fx / self.mass * step_dt
		self.y_vel += fy / self.mass * step_dt
		self.x += self.x_vel * step_dt
		self.y += self.y_vel * step_dt

	def draw(self, display_surface, distance_scale, screen_offset_x=0, screen_offset_y=0):
		x, y = self._screen_position(distance_scale, screen_offset_x, screen_offset_y)

		if 0 <= x <= constants.WIDTH and 0 <= y <= constants.HEIGHT:
			pygame.draw.circle(display_surface, self.color, (int(x), int(y)), max(1, int(self.radius)))
