"""New object model exports."""

import importlib

from .base import Body
from .planet import Planet
from .moon import Moon
from .asteroid import Asteroid


def create_earth(*args, **kwargs):
	module = importlib.import_module("objects.presets.earth")
	return module.create_earth(*args, **kwargs)


def create_moon(*args, **kwargs):
	module = importlib.import_module("objects.presets.moon")
	return module.create_moon(*args, **kwargs)


def create_sun(*args, **kwargs):
	module = importlib.import_module("objects.presets.sun")
	return module.create_sun(*args, **kwargs)

__all__ = [
	"Body",
	"Planet",
	"Moon",
	"Asteroid",
	"create_earth",
	"create_moon",
	"create_sun",
]
