"""Create a simple stationary Sun-Earth system."""

import constants
from objects.base import Body


SUN_EARTH_PIXEL_DISTANCE = 350
SUN_RADIUS_PX = 2
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

    # Use physical units for the Earth position so the physics engine advances it
    earth_distance_m = constants.BODIES_DATA.get("Earth", {}).get("position", 1.0) * constants.AU
    earth = Body(
        -earth_distance_m,
        0,
        EARTH_RADIUS_PX,
        constants.BODIES_DATA["Earth"]["mass"],
        name="Earth",
        color=constants.COLOR_EARTH,
    )
    # Make Earth dynamic so it orbits the Sun under physics
    earth.static_body = False
    earth.draw_line = True
    earth.child_of = sun
    earth.parent_body = sun
    sun.children.append(earth)

    earth.y_vel = constants.BODIES_DATA["Earth"]["orbital_velocity"]

    return [sun, earth]
