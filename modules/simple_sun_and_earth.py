"""Create a simple stationary Sun-Earth system."""

import constants
from objects.base import Body


SUN_EARTH_PIXEL_DISTANCE = 350
SUN_RADIUS_PX = 20
EARTH_RADIUS_PX = 10


def create_sun_and_earth_system():
    sun = Body(
        0,
        0,
        SUN_RADIUS_PX,
        constants.sun_mass,
        name="Sun",
        color=constants.COLOR_SUN,
        is_sun=True,
    )
    sun.static_body = True
    sun.draw_line = False

    earth = Body(
        SUN_EARTH_PIXEL_DISTANCE,
        0,
        EARTH_RADIUS_PX,
        constants.BODIES_DATA["Earth"]["mass"],
        name="Earth",
        color=constants.COLOR_EARTH,
    )
    earth.static_body = True
    earth.draw_line = False
    earth.child_of = sun
    earth.parent_body = sun
    sun.children.append(earth)

    return [sun, earth]
