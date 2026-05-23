"""Create a simple stationary Sun-Earth-Moon system."""

from objects.base import Body

import constants

earth_radius_ratio = (
    constants.BODIES_DATA["Earth"]["radius"] / constants.BODIES_DATA["Moon"]["radius"]
)

# # Keep 1 AU fixed in this preset (with base_scale = 1.0 in app.py)
# SUN_EARTH_PIXEL_DISTANCE = constants.DEFAULT_SCALE * constants.AU # Scale the actual distance to pixels == 350 pixels for 1 AU at default scale

# # Moon boost factor for visibility
# MOON_DISTANCE_VISUAL_FACTOR = 30.0
# EARTH_MOON_PIXEL_DISTANCE = (
#     SUN_EARTH_PIXEL_DISTANCE * (constants.MOON_DATA["perigee"] / constants.AU)
# ) * MOON_DISTANCE_VISUAL_FACTOR

# SUN_RADIUS_PX = 2
# EARTH_RADIUS_PX = constants.BASE_SIZE
# MOON_RADIUS_PX = constants.BASE_SIZE / earth_radius_ratio 


def create_sun_earth_moon_system(
    sun_earth_px=350,
    earth_moon_ratio=0.257,  # Actual Earth-Moon distance ratio to Sun-Earth distance
    earth_radius_px=constants.BASE_SIZE,
    sun_radius_px=2,
):
    earth_moon_px = sun_earth_px * earth_moon_ratio
    moon_radius_px = max(1, int(earth_radius_px / earth_radius_ratio))

    sun = Body(
        0, 0, sun_radius_px, constants.sun_mass,
        name="Sun", color=constants.COLOR_SUN, is_sun=True,
    )
    sun.static_body = True
    sun.draw_line = False

    earth = Body(
        sun_earth_px, 0, earth_radius_px, constants.BODIES_DATA["Earth"]["mass"],
        name="Earth", color=constants.COLOR_EARTH,
    )
    earth.static_body = True
    earth.draw_line = False
    earth.child_of = sun
    earth.parent_body = sun
    sun.children.append(earth)

    moon = Body(
        earth.x + earth_moon_px, 0, moon_radius_px, constants.MOON_DATA["mass"],
        name="Moon", color=constants.MOON_DATA["color"],
    )
    moon.static_body = True
    moon.draw_line = False
    moon.child_of = earth
    moon.parent_body = earth
    earth.children.append(moon)

    return [sun, earth, moon]
