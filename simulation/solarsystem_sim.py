"""Backwards-compatible legacy module for the old simulation API."""

from __future__ import annotations

import constants

from objects.base import Body as Body
from objects.moon import Moon as Moon
from objects.planet import Planet as Planet
from simulation.physics import circular_orbital_speed


class Sun(Body):
	def __init__(self, x, y, radius, mass):
		super().__init__(x, y, radius, mass, name="Sun", color=constants.COLOR_SUN, is_sun=True)
		self.orbit_count = 0


__all__ = [
	"Body",
	"Moon",
	"Planet",
	"Sun",
	"circular_orbital_speed",
]