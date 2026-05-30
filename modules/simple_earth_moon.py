"""Create a simple Earth-Moon system."""

from objects.base import Body

import constants

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
    earth.original_radius = EARTH_RADIUS_PX

    moon_distance = constants.MOON_DATA["average_distance"]
    moon = Body(
        -moon_distance,
        0,
        MOON_RADIUS_PX,
        constants.MOON_DATA["mass"],
        name="Moon",
        color=constants.MOON_DATA["color"],
    )
    moon.static_body = False
    moon.draw_line = True
    moon.child_of = earth
    moon.parent_body = earth
    earth.children.append(moon)
    moon.original_radius = MOON_RADIUS_PX

    moon.y_vel = constants.MOON_DATA["orbital_velocity"]
    
    return [earth, moon]
