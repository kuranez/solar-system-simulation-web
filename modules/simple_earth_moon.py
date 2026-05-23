"""Create a simple stationary Earth-Moon system."""

from objects.base import Body

import constants


EARTH_MOON_PIXEL_DISTANCE = 350
EARTH_RADIUS_PX = 18
MOON_RADIUS_PX = 5


def create_earth_moon_system():
    earth = Body(
        0,
        0,
        EARTH_RADIUS_PX,
        constants.BODIES_DATA["Earth"]["mass"],
        name="Earth",
        color=constants.COLOR_EARTH,
    )
    earth.static_body = True
    earth.draw_line = False

    moon = Body(
        EARTH_MOON_PIXEL_DISTANCE,
        0,
        MOON_RADIUS_PX,
        constants.MOON_DATA["mass"],
        name="Moon",
        color=constants.MOON_DATA["color"],
    )
    moon.static_body = True
    moon.draw_line = False
    moon.child_of = earth
    moon.parent_body = earth
    earth.children.append(moon)

    return [earth, moon]
