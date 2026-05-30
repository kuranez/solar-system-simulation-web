"""Create a simple stationary Sun-Earth-Moon system."""

from objects.base import Body
from simulation.scene import SUN_EARTH_MOON_SCENE

import constants

def create_sun_earth_moon_system():
    """Create a dynamic Sun-Earth-Moon system using SI units for positions.

    Positions are specified in meters so the physics engine advances bodies
    correctly. Radii remain in pixels for rendering.
    """
    sun_radius_px = SUN_EARTH_MOON_SCENE["sun_radius_px"]
    earth_radius_px = SUN_EARTH_MOON_SCENE["earth_radius_px"]
    moon_radius_px = SUN_EARTH_MOON_SCENE["moon_radius_px"]

    # Place Sun at origin (meters)
    sun = Body(0.0, 0.0, sun_radius_px, constants.sun_mass, name="Sun", color=constants.COLOR_SUN, is_sun=True)
    sun.static_body = True
    sun.draw_line = False

    sun.original_radius = sun_radius_px

    # Earth at 1 AU from Sun (meters)
    earth_x_m = -constants.AU
    earth = Body(earth_x_m, 0.0, earth_radius_px, constants.BODIES_DATA["Earth"]["mass"], name="Earth", color=constants.COLOR_EARTH)
    earth.static_body = False
    earth.draw_line = True
    earth.child_of = sun
    earth.parent_body = sun
    sun.children.append(earth)

    earth.original_radius = earth_radius_px

    # Give Earth the approximate orbital velocity around the Sun
    earth.y_vel = constants.BODIES_DATA["Earth"]["orbital_velocity"]
    # Use a smaller integration timestep for Earth and Moon to keep close-orbit
    # dynamics stable (seconds). Default TIMESTEP is 86400 (1 day); use 3600s (1 hour).
    earth.TIMESTEP = 600.0

    # Moon positioned relative to Earth using average distance (meters)
    moon_x_m = earth_x_m - constants.MOON_DATA["average_distance"]
    moon = Body(moon_x_m, 0.0, moon_radius_px, constants.MOON_DATA["mass"], name="Moon", color=constants.MOON_DATA["color"])
    moon.static_body = False
    moon.draw_line = True
    moon.child_of = earth
    moon.parent_body = earth
    earth.children.append(moon)

    moon.original_radius = moon_radius_px

    # Moon's velocity should be Earth velocity plus the Moon's orbital velocity around Earth
    moon.y_vel = earth.y_vel + constants.MOON_DATA["orbital_velocity"]
    moon.TIMESTEP = 600.0

    return [sun, earth, moon]
