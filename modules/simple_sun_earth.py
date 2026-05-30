"""Create a simple Sun-Earth system using object presets."""

import constants
from simulation.scene import SUN_EARTH_SCENE

from objects import create_sun, create_earth

def create_sun_earth_system():
    sun = create_sun()
    if sun is None:
        return []

    # Keep Sun fixed in this simple view, but still expose the hierarchy
    # through parent/child links for the HUD.
    sun.static_body = True
    sun.draw_line = False
    sun.x = 0
    sun.y = 0
    sun.original_radius = SUN_EARTH_SCENE["sun_radius_px"]

    earth = create_earth()
    earth.static_body = False
    earth.draw_line = True
    earth.child_of = sun
    earth.parent_body = sun
    sun.children.append(earth)
    earth.original_radius = SUN_EARTH_SCENE["earth_radius_px"]
    earth.y_vel = SUN_EARTH_SCENE["earth_velocity"]

    return [sun, earth]