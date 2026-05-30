"""Create a simple Sun-Earth system using object presets."""

import constants

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
    sun.original_radius = 2

    earth = create_earth()
    earth.static_body = False
    earth.draw_line = True
    earth.child_of = sun
    earth.parent_body = sun
    sun.children.append(earth)
    earth.original_radius = 18
    earth.y_vel = constants.BODIES_DATA["Earth"]["orbital_velocity"]

    return [sun, earth]