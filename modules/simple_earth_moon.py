"""Create a simple Earth-Moon system using object presets."""

import constants
from simulation.scene import EARTH_MOON_SCENE

from objects import create_earth, create_moon


def create_earth_moon_system():
    earth = create_earth()
    if earth is None:
        return []

    # Keep Earth fixed in this simple view, but still expose the hierarchy
    # through parent/child links for the HUD.
    earth.static_body = True
    earth.draw_line = False
    earth.x = 0
    earth.y = 0
    earth.original_radius = EARTH_MOON_SCENE["earth_radius_px"]

    moon = create_moon(earth)
    moon.static_body = False
    moon.draw_line = True
    moon.original_radius = EARTH_MOON_SCENE["moon_radius_px"]
    moon.y_vel = EARTH_MOON_SCENE["moon_velocity"]

    return [earth, moon]
