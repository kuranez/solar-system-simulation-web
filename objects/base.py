"""Shared base body implementation for the new object model."""

from __future__ import annotations

import math
import pygame

import constants
from simulation import physics


class Body:
	AU = constants.AU
	G = constants.G
	TIMESTEP = constants.TIMESTEP

	def __init__(self, x, y, radius, mass, name="Body", color=(0, 0, 0), is_sun=False):
		self.x = x
		self.y = y
		self.original_x = x
		self.original_y = y
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
		self.orbit_start_index = 0
		self.last_complete_orbit = []
		self.orbit_detected = False
		self.orbit_last_angle = None
		self.orbit_angle_accumulator = 0.0
		self.orbit_samples_since_completion = 0
		self.orbit_completion_cooldown = 0
		# Transient HUD flash timer (frames) set when an orbit completes
		self.orbit_complete_flash = 0
		self.prev_x = x
		self.prev_y = y
		self.x_vel = 0.0
		self.y_vel = 0.0
		self.draw_line = True
		# Children bodies (moons, rings, etc.) — factories should append here
		self.children = []

	def update_distance_to_sun(self, sun):
		physics.update_distance_to_sun(self, sun)

	def attraction(self, other):
		return physics.attraction(self, other)

	def update_position(self, current_solarsystem):
		physics.advance_body(self, current_solarsystem)

		# Decrement any transient HUD flash timer (presentations/rendering run per-frame)
		if getattr(self, "orbit_complete_flash", 0) > 0:
			self.orbit_complete_flash -= 1

	def _check_orbit_completion(self, current_solarsystem=None):
		# Compute current point in the same reference frame used when recording orbit points
		parent_body = getattr(self, "parent_body", None)
		if parent_body is not None:
			ref_x = parent_body.x
			ref_y = parent_body.y
		else:
			# Try to find the system sun if available
			ref = None
			if current_solarsystem is not None:
				from simulation.physics import find_sun
				ref = find_sun(current_solarsystem)
			if ref is not None:
				ref_x = ref.x
				ref_y = ref.y
			else:
				ref_x = 0
				ref_y = 0

		current_point = (self.x - ref_x, self.y - ref_y)

		current_angle = math.atan2(current_point[1], current_point[0])
		if self.orbit_last_angle is None:
			self.orbit_last_angle = current_angle
			return

		# Unwrap the angular delta into [-pi, pi] so the accumulator behaves smoothly.
		angle_delta = current_angle - self.orbit_last_angle
		if angle_delta > math.pi:
			angle_delta -= 2 * math.pi
		elif angle_delta < -math.pi:
			angle_delta += 2 * math.pi

		self.orbit_angle_accumulator += angle_delta
		self.orbit_last_angle = current_angle
		self.orbit_samples_since_completion += 1

		# Count one full revolution once the unwrapped angle reaches 2π.
		if (
			not self.orbit_detected
			and self.orbit_samples_since_completion > 12
			and abs(self.orbit_angle_accumulator) >= 2 * math.pi
		):
			self.orbit_count += 1
			self.orbit_detected = True
			self.last_complete_orbit = list(self.orbit)
			if self.last_complete_orbit:
				self.last_complete_orbit.append(self.last_complete_orbit[0])
			self.orbit = [current_point]
			self.orbit_start_index = 0
			self.orbit_angle_accumulator = 0.0
			self.orbit_samples_since_completion = 0
			self.orbit_completion_cooldown = 12
			try:
				self.orbit_complete_flash = 180
			except Exception:
				pass

		if self.orbit_detected and self.orbit_completion_cooldown > 0:
			self.orbit_completion_cooldown -= 1
			if self.orbit_completion_cooldown <= 0:
				self.orbit_detected = False

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

	def _complete_orbit_points(self, distance_scale, screen_offset_x=0, screen_offset_y=0):
		points = []
		if self.last_complete_orbit:
			points.extend(
				(
					px * distance_scale + screen_offset_x,
					py * distance_scale + screen_offset_y,
				)
				for px, py in self.last_complete_orbit
			)
		return points

	def _draw_point_trail(self, display_surface, orbit_points, fade_scale=1.5):
		if len(orbit_points) < 2:
			return

		for i in range(1, len(orbit_points)):
			distance = len(orbit_points) - i
			fade_factor = max(0, min(255, int(255 * (distance / len(orbit_points)) * fade_scale)))
			faded_color = (
				int(self.color[0] * (1 - fade_factor / 255) + constants.COLOR_BACKGROUND[0] * (fade_factor / 255)),
				int(self.color[1] * (1 - fade_factor / 255) + constants.COLOR_BACKGROUND[1] * (fade_factor / 255)),
				int(self.color[2] * (1 - fade_factor / 255) + constants.COLOR_BACKGROUND[2] * (fade_factor / 255)),
			)
			pygame.draw.line(display_surface, faded_color, orbit_points[i - 1], orbit_points[i], 1)

	def _draw_orbit_trail(self, display_surface, distance_scale, screen_offset_x=0, screen_offset_y=0, fade_scale=1.0, completed_fade_scale=0.7):
		if not self.draw_line:
			return

		completed_points = self._complete_orbit_points(distance_scale, screen_offset_x, screen_offset_y)
		self._draw_point_trail(display_surface, completed_points, completed_fade_scale)

		current_points = self._orbit_points(distance_scale, screen_offset_x, screen_offset_y)
		self._draw_point_trail(display_surface, current_points, fade_scale)

	def draw(self, display_surface, distance_scale, screen_offset_x=0, screen_offset_y=0):
		x, y = self._screen_position(distance_scale, screen_offset_x, screen_offset_y)
		self._draw_orbit_trail(display_surface, distance_scale, screen_offset_x, screen_offset_y)
		pygame.draw.circle(display_surface, self.color, (int(x), int(y)), max(1, int(self.radius)))
